import socket
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Host:
    def __init__(self, host_id, host_ip, host_port, router_ip, router_port):
        self.host_id = host_id
        self.host_ip = host_ip
        self.host_port = host_port
        self.router_ip = router_ip
        self.router_port = router_port

    def connect_to_router(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.host_ip, self.host_port))

        try:
            client_socket.connect((self.router_ip, self.router_port))
            print(f"Conectado al router {self.router_ip}:{self.router_port}")

            # Crear un JSON con la IP, puerto e ID del host
            host_info = {
                "host_id": self.host_id,
                "host_ip": self.host_ip,
                "host_port": self.host_port
            }
            host_info_json = json.dumps(host_info)

            # Enviar el JSON al router
            client_socket.send(host_info_json.encode('utf-8'))

            # Recibir la longitud del mensaje primero
            message_length = int.from_bytes(client_socket.recv(4), byteorder='big')
            data = b''
            while len(data) < message_length:
                fragment = client_socket.recv(1024)
                if not fragment:
                    break
                data += fragment

            print(f"Recibido: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            client_socket.close()

    def __repr__(self):
        return f"Host(ID={self.host_id}, Router IP={self.router_ip})"
