import socket
import ssl
import json

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket a la dirección y puerto
server_socket.bind(('localhost', 60000))
server_socket.listen(5)

# Envolver el socket con SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="../certificate/server.crt", keyfile="../certificate/server.key")
#print(ssl._create_unverified_context())
print("Servidor escuchando en el puerto 60000...")

# Aceptar conexiones y manejarlas
while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión desde {addr}")
    try:
        # Asegurar el socket
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        # Recibir datos del router
        data = secure_socket.recv(1024).decode('utf-8')
        print(f"Recibido: {data}")

        # Preparar y enviar una respuesta (en este caso, una ruta ficticia)
        route_info = {
            "routes": [
                {"src": "A", "dst": "B", "path": ["A", "C", "B"], "cost": 10},
                {"src": "A", "dst": "D", "path": ["A", "D"], "cost": 5}
            ]
        }
        response = json.dumps(route_info)
        secure_socket.sendall(response.encode('utf-8'))
    except ssl.SSLError as ssl_err:
        print(f"Error SSL al conectar: {ssl_err}")
    except Exception as e:
        print(f"Error al conectar: {e}")
    finally:
        secure_socket.close()
