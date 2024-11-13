import socket
import ssl
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar el contenido del archivo routes.json
with open(os.path.join(BASE_DIR, 'routes.json'), 'r') as f:
    route_info = json.load(f)

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 60000))
server_socket.listen(5)

# Configurar SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=os.path.join(BASE_DIR, "../certificate/server.crt"), keyfile=os.path.join(BASE_DIR, "../certificate/server.key"))
print("Servidor escuchando en el puerto 60000...")

def send_large_message(socket, message):
    # Convertir el mensaje a bytes
    message_bytes = message.encode('utf-8')
    message_length = len(message_bytes)
    
    # Enviar la longitud del mensaje primero
    socket.sendall(message_length.to_bytes(4, byteorder='big'))

    # Enviar el mensaje en fragmentos de tamaño 1024
    for i in range(0, message_length, 1024):
        socket.sendall(message_bytes[i:i+1024])

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión desde {addr}")
    try:
        secure_socket = context.wrap_socket(client_socket, server_side=True)
        data = secure_socket.recv(1024).decode('utf-8')
        print(f"Recibido: {data}")

        # Enviar el contenido de routes.json a cada cliente que se conecte
        response = json.dumps(route_info)
        send_large_message(secure_socket, response)
    except ssl.SSLError as ssl_err:
        print(f"Error SSL al conectar: {ssl_err}")
    except Exception as e:
        print(f"Error al conectar: {e}")
    finally:
        secure_socket.close()
