import socket
import json

class Host:
    def __init__(self, host_id, host_ip, host_port, router_ip, router_port):
        self.host_id = host_id
        self.host_ip = host_ip
        self.host_port = host_port
        self.router_ip = router_ip
        self.router_port = router_port

        self.connect_to_router()

    def connect_to_router(self, dest_router_ip=None, dest_router_port=None, message=None):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.host_ip, self.host_port))

        try:
            client_socket.connect((self.router_ip, self.router_port))
            print(f"Conectado al router {self.router_ip}:{self.router_port}")

            if message:
                host_info_json = json.dumps(message)
                client_socket.send(host_info_json.encode('utf-8'))
            else:
                host_info = {
                    "src_host_id": self.host_id,
                    "src_host_port": self.host_port,
                    "newHost": 1
                }
                host_info_json = json.dumps(host_info)
                client_socket.send(host_info_json.encode('utf-8'))

            data = client_socket.recv(1024).decode('utf-8')
            print(f"Recibido: {data}")
        except Exception as e:
            print(f"Error al conectar: {e}")
        finally:
            client_socket.close()

    def __repr__(self):
        return f"Host(ID={self.host_id}, Router IP={self.router_ip})"
