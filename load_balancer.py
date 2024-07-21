# load_balancer.py

from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHash
import requests

app = Flask(__name__)

# Initialize consistent hashing
hash_ring = ConsistentHash()


@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = list(hash_ring.ring.values())
    return jsonify({"N": len(replicas), "replicas": replicas, "status": "successful"}), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get('n', 1)
    hostnames = data.get('hostnames', [])
    
    added_replicas = []
    for _ in range(n):
        if hostnames:
            server_id = hostnames.pop(0)
        else:
            server_id = f"server-{len(hash_ring.ring)}"
        
        hash_ring.add_node(server_id)
        added_replicas.append(server_id)
    
    return jsonify({"message": {"N": len(hash_ring.ring), "replicas": added_replicas}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get('n', 1)
    hostnames = data.get('hostnames', [])
    
    removed_replicas = []
    for _ in range(min(n, len(hash_ring.ring))):
        if hostnames:
            server_id = hostnames.pop(0)
        else:
            server_id = list(hash_ring.ring.values())[0]
        
        hash_ring.remove_node(server_id)
        removed_replicas.append(server_id)
    
    return jsonify({"message": {"N": len(hash_ring.ring), "replicas": removed_replicas}, "status": "successful"}), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server = hash_ring.get_node(path)
    if server:
        response = requests.get(f"http://{server}:5000/{path}")
        return jsonify(response.json()), response.status_code
    return jsonify({"message": f"<Error> '/{path}' endpoint does not exist in server replicas", "status": "failure"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)