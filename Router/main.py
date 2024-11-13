import json
import sys
import os
from Router import Router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    i = int(sys.argv[1])
    links = sys.argv[2].split(',')

    with open(os.path.join(BASE_DIR, 'server.json'), 'r') as f:
        server_config = json.load(f)

    server_ip = server_config["server_ip"]
    server_port = server_config["server_port"]
    router_ip = server_ip
    
    router = Router(
                    router_id=i, 
                    router_ip=router_ip, 
                    router_port=60001 + i, 
                    server_ip=server_ip, 
                    server_port=server_port, 
                    cafile=os.path.join(BASE_DIR, '../certificate/server.crt'),
                    links=links
                    ) 
    print(f"Router {i + 1} connecting to server {server_ip}:{server_port} from port {60001 + i}") 
    router.connect_to_controller()

if __name__ == "__main__":
    main()
