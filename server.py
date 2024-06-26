import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

server_id = int(os.getenv('SERVER_ID', '1'))

@app.route('/home', methods=['GET'])
def home():
    response = {
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
