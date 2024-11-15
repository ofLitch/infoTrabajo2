import sys
import json
import os
from Host import Host

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTS_FILE = os.path.join(BASE_DIR, '../Router/router_ports.json')  # Ajustar la ruta para la carpeta Router

def read_router_port(router_id):
    with open(PORTS_FILE, 'r') as f:
        ports_info = json.load(f)
    return ports_info[str(router_id)]

def main(host_id, router_ip):
    # Leer el puerto del router desde el archivo JSON
    router_port = read_router_port(host_id)

    # Configuración del Host
    host_ip = "127.0.0.1"  # Cambia esto a la IP del host si es necesario
    host_port = 50000 + host_id  # Puerto del Host basado en el ID para evitar conflictos

    # Crear instancia del Host
    host = Host(host_id, host_ip, host_port, router_ip, router_port)
    print(host)

    while True:
        print("\n--- MENÚ ---")
        dest_host_id = int(input("Ingrese el ID del Host de destino: "))
        dest_router_ip = "127.0.0.1"  # input("Ingrese la IP del Router de destino: ")
        msg = input("Ingrese el mensaje a enviar: ")

        # Formar el mensaje a enviar
        message = {
            "src_host_id": host_id,
            "src_host_port": host_port,
            "dest_host_id": dest_host_id,
            "dest_router_ip": dest_router_ip,
            "msg": msg
        }

        # Conectar al Router y enviar el mensaje
        host.connect_to_router(dest_router_ip, router_port, message)

if __name__ == "__main__":
    # Obtener los parámetros del Host y el Router de los argumentos de la línea de comandos
    host_id = int(sys.argv[1])
    router_ip = sys.argv[2]
    main(host_id, router_ip)
