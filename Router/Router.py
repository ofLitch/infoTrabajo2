import socket
import ssl
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Router:
    def __init__(self, router_id, router_ip, router_port, server_ip, server_port, cafile):
        self.router_id = router_id
        self.router_ip = router_ip
        self.router_port = router_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.cafile = cafile
        self.links = []

    def connect_to_controller(self):
        # Crear un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.router_ip, self.router_port))
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(self.cafile)

        try:
            # Conectar al servidor con SSL
            secure_socket = context.wrap_socket(client_socket, server_hostname=self.server_ip)
            secure_socket.connect((self.server_ip, self.server_port))
            print(client_socket)
            print(f"Conectado al servidor {self.server_ip}:{self.server_port}")

            # Crear un JSON con la IP, puerto e ID del router
            router_info = {
                "router_id": self.router_id,
                "router_ip": self.router_ip,
                "router_port": self.router_port
            }
            router_info_json = json.dumps(router_info)

            # Enviar el JSON al servidor
            secure_socket.send(router_info_json.encode('utf-8'))

            # Recibir la longitud del mensaje primero
            message_length = int.from_bytes(secure_socket.recv(4), byteorder='big')
            data = b''
            while len(data) < message_length:
                fragment = secure_socket.recv(1024)
                if not fragment:
                    break
                data += fragment

            print(f"Received route: {data.decode('utf-8')}")

            # Filtrar y almacenar datos de la ruta
            self.store_route(json.loads(data.decode('utf-8')))
        except ssl.SSLError as ssl_err:
            print(f"Error SSL al conectar: {ssl_err}")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            secure_socket.close()

    def store_route(self, route_info):
        routes = route_info['routes']
        # Filtrar enlaces relevantes para este router
        self.links = [route for route in routes if route['src'] == str(self.router_id)]
        with open(os.path.join(BASE_DIR, f'router_{self.router_id}_routes.json'), 'w') as json_file:
            json.dump(self.links, json_file)
            print(f"Routes stored in router_{self.router_id}_routes.json")

    def evaluate_performance(self):
        # Implementar lógica de evaluación de desempeño
        pass

    def __repr__(self):
        return f"Router(ID={self.router_id}, Server IP={self.server_ip})"
