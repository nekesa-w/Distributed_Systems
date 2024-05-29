import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from consistenthashing import ConsistentHashMap

class LoadBalancerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.consistent_hash = ConsistentHashMap(512, 9)
        self.server_containers = {}
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/rep':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': {'N': len(self.consistent_hash.hash_map), 'eplicas': list(self.consistent_hash.hash_map.values())}}
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith('/add'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            for i in range(payload['n']):
                server_id = payload['hostnames'][i]
                self.consistent_hash.add_server(server_id)
                self.server_containers[server_id] = {'name': server_id, 'tatus': 'up'}
                os.system(f'docker run -d --name {server_id} --network net1 --network-alias {server_id} server:latest')
            response = {'message': f'Added {payload["n"]} new server instances'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith('/rm'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            for i in range(payload['n']):
                server_id = payload['hostnames'][i]
                self.consistent_hash.remove_server(server_id)
                if server_id in self.server_containers:
                    os.system(f'docker stop {server_id} && docker rm {server_id}')
                    del self.server_containers[server_id]
            response = {'message': f'Removed {payload["n"]} server instances'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith('/'):
            request_id = int(self.path[1:])
            server_id = self.consistent_hash.get_server(request_id)
            if server_id:
                if server_id in self.server_containers and self.server_containers[server_id]['status'] == 'up':
                    self.send_response(302)
                    self.send_header('Location', f'http://{server_id}:5000{self.path}')
                    self.end_headers()
                else:
                    self.send_response(503)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Server instance is down')
            else:
                self.send_response(503)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Server instance not found')

def run_load_balancer():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, LoadBalancerHandler)
    print('Starting load balancer...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_load_balancer()

