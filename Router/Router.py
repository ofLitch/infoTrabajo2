import socket
import ssl
import os
import json
import threading

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

        # Conectar al controlador una vez usando SSL
        self.connect_to_controller()

    def connect_to_controller(self, host_info=None):
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
                "router_port": self.router_port
            }

            if host_info:
                router_info['host'] = host_info

            router_info_json = json.dumps(router_info)
            secure_socket.send(router_info_json.encode('utf-8'))

            message_length = int.from_bytes(secure_socket.recv(4), byteorder='big')
            data = b''
            while len(data) < message_length:
                fragment = secure_socket.recv(1024)
                if not fragment:
                    break
                data += fragment

            print(f"Received route: {data.decode('utf-8')}")
            self.store_route(json.loads(data.decode('utf-8')))
        except ssl.SSLError as ssl_err:
            print(f"Error SSL al conectar: {ssl_err}")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            secure_socket.close()

    def store_route(self, route_info):
        routes = route_info['routes']
        self.links = [route for route in routes if route['src'] == str(self.router_id)]
        with open(os.path.join(BASE_DIR, f'router_{self.router_id}_routes.json'), 'w') as json_file:
            json.dump(self.links, json_file)
            print(f"Routes stored in router_{self.router_id}_routes.json")

    def start_listening(self):
        # Crear un socket para escuchar las conexiones de hosts
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.router_ip, self.router_port))
        server_socket.listen(5)

        print(f"Router {self.router_id} escuchando en {self.router_ip}:{self.router_port}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión desde {addr}")
            try:
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Recibido: {data}")

                # Procesar datos recibidos de los hosts y enviar al controller usando SSL
                dataTemp = json.loads(data)
                self.connect_to_controller(dataTemp)
            except Exception as e:
                print(f"Error al procesar conexión: {e}")
            finally:
                client_socket.close()

    def __repr__(self):
        return f"Router(ID={self.router_id}, Server IP={self.server_ip})"
