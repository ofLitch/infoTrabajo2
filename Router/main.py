import json
from Router import Router

# Código de prueba para instanciar routers y conectarlos al controlador
def main():
    # Leer configuración del servidor desde server.json
    with open('server.json', 'r') as f:
        server_config = json.load(f)

    server_ip = server_config["server_ip"]
    server_port = server_config["server_port"]
    router_ip = server_ip
    
    for i in range(0, 23):
        router_port = 40001 + i
        router = Router(router_id=i + 1, 
                        router_ip=router_ip, 
                        router_port=router_port, 
                        server_ip=server_ip, 
                        server_port=server_port, 
                        cafile='../certificate/server.crt')
        print(f"Router {i + 1} connecting to server {server_ip}:{server_port} from port {router_port}")
        router.connect_to_controller()
        router.evaluate_performance()

if __name__ == "__main__":
    main()
