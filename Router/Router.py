import socket
import ssl
import json

class Router:
    def __init__(self, router_id, router_ip, router_port, server_ip, server_port, cafile):
        self.router_id = router_id
        self.router_ip = router_ip
        self.router_port = router_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.cafile = cafile
        self.routes = {}

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

            # Enviar y recibir datos
            message = f"Hello, Secure Server! Router: {self.router_id}"
            secure_socket.send(message.encode('utf-8'))
            data = secure_socket.recv(1024)
            print(f"Received route: {data.decode('utf-8')}")

            # Almacenar datos de la ruta
            self.store_route(json.loads(data.decode('utf-8')))
        except ssl.SSLError as ssl_err:
            print(f"Error SSL al conectar: {ssl_err}")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            secure_socket.close()

    def store_route(self, route):
        self.routes = route
        with open(f'router_{self.router_id}_routes.json', 'w') as json_file:
            json.dump(self.routes, json_file)
            print(f"Routes stored in router_{self.router_id}_routes.json")

    def evaluate_performance(self):
        # Implementar lógica de evaluación de desempeño
        pass

    def __repr__(self):
        return f"Router(ID={self.router_id}, Server IP={self.server_ip})"
