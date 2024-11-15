import socket
import ssl
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTS_FILE = os.path.join(BASE_DIR, 'router_ports.json')

class Router:
    def __init__(self, router_id, router_ip, router_port, server_ip, server_port, cafile):
        self.router_id = router_id
        self.router_ip = router_ip
        self.router_port = router_port  # Puerto fijo definido al iniciar el Router
        self.server_ip = server_ip
        self.server_port = server_port
        self.cafile = cafile
        self.links = []
        self.hosts = {}

        self.server_socket = None

    def save_port(self):
        """Guardar el puerto en un archivo JSON para persistencia."""
        if os.path.exists(PORTS_FILE):
            with open(PORTS_FILE, 'r') as f:
                ports_info = json.load(f)
        else:
            ports_info = {}
        ports_info[self.router_id] = self.router_port
        with open(PORTS_FILE, 'w') as f:
            json.dump(ports_info, f)

    def connect_to_controller(self, message=None, initial_host=False, dest_router_id=None):
        """Conectar al controlador y solicitar rutas."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(self.cafile)
        try:
            secure_socket = context.wrap_socket(client_socket, server_hostname=self.server_ip)
            secure_socket.connect((self.server_ip, self.server_port))
            print(f"Conectado al servidor {self.server_ip}:{self.server_port}")

            router_info = {
                "router_id": self.router_id,
                "router_ip": self.router_ip,
                "router_port": self.router_port,
                "hosts": self.hosts
            }

            if message:
                router_info['message'] = message
                if initial_host:
                    self.hosts[str(message['src_host_id'])] = {
                        'src_host_id': message['src_host_id'],
                        'src_host_port': message['src_host_port']
                    }
                if dest_router_id:
                    router_info['message']['dest_router_id'] = dest_router_id

            secure_socket.send(json.dumps(router_info).encode('utf-8'))

            message_length = int.from_bytes(secure_socket.recv(4), byteorder='big')
            data = b''
            while len(data) < message_length:
                fragment = secure_socket.recv(1024)
                if not fragment:
                    break
                data += fragment

            route_info = json.loads(data.decode('utf-8'))
            print(f"Ruta recibida del Controller: {route_info}")

            if 'path' in route_info and 'routers' in route_info:
                if route_info['destination'] != self.router_id:
                    print("Reenviando mensaje a través de forward_message.")
                    self.forward_message(route_info)  # Reenvío al siguiente router
                else:
                    self.deliver_message_to_host(route_info['message'])
            else:
                print("Error: route_info no contiene 'path' o 'routers'")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            secure_socket.close()

    def forward_message(self, route_info):
        """Reenviar el mensaje al siguiente router en la ruta."""
        if 'message' in route_info and 'path' in route_info:
            next_hop_router_id = route_info['path'][1]  # El siguiente hop en el camino
            next_hop_info = route_info['routers'].get(str(next_hop_router_id), {})

            next_router_ip = next_hop_info.get('router_ip', None)
            next_router_port = next_hop_info.get('router_port', None)

            if not next_router_ip or not next_router_port:
                print(f"Error: No se encontró la IP o el puerto para el siguiente router ({next_hop_router_id}) en la ruta.")
                return

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client_socket.connect((next_router_ip, next_router_port))
                print(f"Reenviando mensaje a {next_router_ip}:{next_router_port}")

                message_json = json.dumps(route_info)
                print(f"Mensaje a reenviar: {message_json}")  # Verificar el mensaje

                client_socket.send(message_json.encode('utf-8'))
                print(f"Mensaje reenviado: {route_info['message']}")
            except Exception as e:
                print(f"Error al reenviar el mensaje: {e}")
            finally:
                client_socket.close()
        else:
            print("Error: route_info no contiene 'message' o 'path'")

    def start_listening(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.router_ip, self.router_port))
        self.server_socket.listen(5)

        self.save_port()  # Guardar el puerto
        self.connect_to_controller()  # Registro inicial con el controlador

        print(f"Router {self.router_id} escuchando en {self.router_ip}:{self.router_port}...")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión desde {addr}")

            try:
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Recibido: {data}")

                if not data:
                    print("Error: Mensaje vacío recibido")
                    continue

                message = json.loads(data)

                if 'message' in message:
                    if str(self.router_id) == str(message['destination']):
                        print(f"Soy el destino final del mensaje.")
                        self.deliver_message_to_host(message)
                    else:
                        print(f"Solicitando rutas para reenviar paquete al router destino {message['dest_router_id']}.")
                        self.connect_to_controller(message)  # Solicitar ruta al Controller
                else:
                    print(f"Registrando el host {message['src_host_id']} al controller.")
                    self.connect_to_controller(message, initial_host=True)
            except json.JSONDecodeError:
                print("Error al decodificar el mensaje JSON recibido")
            except Exception as e:
                print(f"Error al procesar conexión: {e}")
            finally:
                client_socket.close()

    def deliver_message_to_host(self, message):
        print(message)
        host_ip = message['message']['dest_router_ip']
        host_port = message['message']['dest_host_port']
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            print(f"Conectando al host en {host_ip}:{host_port}")  # Mensaje de depuración
            client_socket.connect((host_ip, host_port))
            print(f"Entregando mensaje al host en {host_ip}:{host_port}")

            message_json = json.dumps(message)
            client_socket.send(message_json.encode('utf-8'))

            print(f"Mensaje entregado al host: {message}")
        except Exception as e:
            print(f"Error al entregar el mensaje al host: {e}")
        finally:
            client_socket.close()


    def __repr__(self):
        return f"Router(ID={self.router_id}, Server IP={self.server_ip})"
