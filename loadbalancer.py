# load_balancer.py

from flask import Flask, request, jsonify
from consistenthashing import ConsistentHashMap
import os
import random

app = Flask(__name__)
hashing = ConsistentHashMap()
servers = []

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"N": len(servers), "replicas": servers, "status": "successful"}), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400
    
    for hostname in hostnames:
        servers.append(hostname)
        hashing.add_server(hostname)

    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400
    
    for hostname in hostnames:
        if hostname in servers:
            servers.remove(hostname)
            hashing.remove_server(hostname)

    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/<path>', methods=['GET'])
def route_request(path):
    server = hashing.get_server(path)
    if server:
        return jsonify({"message": f"Routing to {server}", "status": "successful"}), 200
    return jsonify({"message": "<Error> Endpoint does not exist", "status": "failure"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

