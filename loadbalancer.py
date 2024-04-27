from flask import Flask, request, jsonify
import json
import random
from consistent_hash_map import ConsistentHashMap

loadbalancer = Flask(__name__)
chm = ConsistentHashMap()

@loadbalancer.route('/rep', methods=['GET'])
def get_replicas():
    replicas = list(chm.servers.keys())
    return jsonify(message={"N": len(replicas), "replicas": replicas}, status="successful"), 200

@loadbalancer.route('/add', methods=['POST'])
def add_server():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) != n:
        return jsonify(message="Length of hostname list does not match the number of instances to be added", status="failure"), 400
    
    for hostname in hostnames:
        chm.add_server(hostname)
    
    return jsonify(message={"N": len(chm.servers), "replicas": list(chm.servers.keys())}, status="successful"), 200

@loadbalancer.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
     if len(hostnames) != n:
        return jsonify(message="Length of hostname list does not match the number of instances to be added", status="failure"), 400

    for hostname in hostnames:
        chm.remove_server(hostname)
    
    return jsonify(message={"N": len(chm.servers), "replicas": list(chm.servers.keys())}, status="successful"), 200

@loadbalancer.route('/path:path', methods=['GET'])
def proxy_request(path):
"""Route incoming requests to the appropriate server based on consistent hashing."""
    server_id = chm.get_server(path)

    if server_id:
        return jsonify(message=f"Request routed to {server_id}"), 200
    else:
        return jsonify(message="No server available"), 503

if name == 'main':
app.run(host='0.0.0.0', port=5000, debug=True)
