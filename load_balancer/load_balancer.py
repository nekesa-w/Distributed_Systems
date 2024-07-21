from flask import Flask, jsonify, request
import docker
from consistent_hash import ConsistentHash
import requests
import random
import string
import time

app = Flask(__name__)
client = docker.from_env()
ch = ConsistentHash()

server_request_counts = {}

# Initialize with 3 server instances
for i in range(3):
    server_name = f"server_{i}"
    client.containers.run("server_image", detach=True, name=server_name, network="load_balancer_network")
    ch.add_server(server_name)
    server_request_counts[server_name] = 0

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = list(ch.servers.keys())
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    for i in range(n):
        server_name = hostnames[i] if i < len(hostnames) else f"server_{random.randint(1000, 9999)}"
        client.containers.run("server_image", detach=True, name=server_name, network="load_balancer_network")
        ch.add_server(server_name)
        server_request_counts[server_name] = 0
    
    return jsonify({"message": f"{n} servers added", "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    removed = 0
    for server in list(ch.servers.keys()):
        if removed >= n:
            break
        if not hostnames or server in hostnames:
            ch.remove_server(server)
            client.containers.get(server).stop()
            client.containers.get(server).remove()
            del server_request_counts[server]
            removed += 1
    
    return jsonify({"message": f"{removed} servers removed", "status": "successful"}), 200

@app.route('/<path>', methods=['GET'])
def route_request(path):
    request_id = random.randint(100000, 999999)
    server = ch.get_server(request_id)
    server_request_counts[server] += 1
    
    try:
        response = requests.get(f"http://{server}:5000/{path}", timeout=5)
        return response.content, response.status_code
    except requests.RequestException:
        return jsonify({"error": "Server unavailable"}), 503

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(server_request_counts)

@app.route('/simulate_failure', methods=['POST'])
def simulate_failure():
    server_to_fail = request.json['server']
    start_time = time.time()
    
    ch.remove_server(server_to_fail)
    client.containers.get(server_to_fail).stop()
    client.containers.get(server_to_fail).remove()
    del server_request_counts[server_to_fail]
    
    new_server_name = f"server_{random.randint(1000, 9999)}"
    client.containers.run("server_image", detach=True, name=new_server_name, network="load_balancer_network")
    ch.add_server(new_server_name)
    server_request_counts[new_server_name] = 0
    
    end_time = time.time()
    recovery_time = end_time - start_time
    
    return jsonify({"recovery_time": recovery_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)