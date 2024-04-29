from flask import Flask, request, jsonify
import json
import random
from consistent_hash_map import ConsistentHashMap
import asyncio
import aiohttp
import matplotlib.pyplot as plt

app = Flask(__name__)
chm = ConsistentHashMap()

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = list(chm.servers.keys())
    return jsonify(message={"N": len(replicas), "replicas": replicas}, status="successful"), 200

@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) != n:
        return jsonify(message="Length of hostname list does not match the number of instances to be added", status="failure"), 400
    
    for hostname in hostnames:
        chm.add_server(hostname)
    
    return jsonify(message={"N": len(chm.servers), "replicas": list(chm.servers.keys())}, status="successful"), 200

@app.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.json
    hostnames = data.get('hostnames', [])
    
    for hostname in hostnames:
        chm.remove_server(hostname)
    
    return jsonify(message={"N": len(chm.servers), "replicas": list(chm.servers.keys())}, status="successful"), 200

@app.route('/path:path', methods=['GET'])
def proxy_request(path):

#Route incoming requests to the appropriate server based on consistent hashing
    
server_id = chm.get_server(path)
if server_id:
return jsonify(message=f"Request routed to {server_id}"), 200
else:
return jsonify(message="No server available"), 503
if name == 'main':
app.run(host='0.0.0.0', port=5000, debug=True)


#Analysis
# Launch 10,000 async requests on N = 3 server containers
async def send_requests(num_requests, load_balancer_url):
    server_counts = {f"Server {i}": 0 for i in range(1, 4)}
    async with aiohttp.ClientSession() as session:
        async def fetch(session, url):
            async with session.get(url) as response:
                server_id = (await response.text()).split(":")[1].strip()
                server_counts[server_id] += 1

        await asyncio.gather(*[fetch(session, f"{load_balancer_url}/home") for _ in range(num_requests)])

    fig, ax = plt.subplots()
    ax.bar(server_counts.keys(), server_counts.values())
    ax.set_title("Request Distribution (N = 3)")
    ax.set_xlabel("Server Instance")
    ax.set_ylabel("Request Count")
    plt.show()

# Increment N from 2 to 6 and launch 10,000 requests on each increment
async def send_requests_varying_n(num_requests, load_balancer_url, add_endpoint):
    average_loads = []
    for n in range(2, 7):
        async with aiohttp.ClientSession() as session:
            await session.post(add_endpoint, json={"n": n})

            server_counts = {f"Server {i}": 0 for i in range(1, n + 1)}
            async def fetch(session, url):
                async with session.get(url) as response:
                    server_id = (await response.text()).split(":")[1].strip()
                    server_counts[server_id] += 1

            await asyncio.gather(*[fetch(session, f"{load_balancer_url}/home") for _ in range(num_requests)])
            average_load = num_requests / n
            average_loads.append(average_load)

    fig, ax = plt.subplots()
    ax.plot(range(2, 7), average_loads)
    ax.set_title("Average Load vs N")
    ax.set_xlabel("Number of Server Instances (N)")
    ax.set_ylabel("Average Load")
    plt.show()

# Test all endpoints of the load balancer and show recovery from server failure
async def test_endpoints(load_balancer_url, rep_endpoint, add_endpoint, rm_endpoint):
    async with aiohttp.ClientSession() as session:
        # Test /rep endpoint
        async with session.get(rep_endpoint) as response:
            print(await response.text())

        # Test /rm endpoint
        await session.delete(rm_endpoint, json={"n": 1})

        # Test /<path> endpoint after removing a server instance
        async with session.get(f"{load_balancer_url}/home") as response:
            print(await response.text())

        # Test /add endpoint
        await session.post(add_endpoint, json={"n": 1})

        # Test /<path> endpoint after adding a new server instance
        async with session.get(f"{load_balancer_url}/home") as response:
            print(await response.text())

# Modify the hash functions and report observations
# (Implement hash function modifications and repeat Tasks 1 and 2)

if __name__ == "__main__":
    load_balancer_url = "http://localhost:5000"
    rep_endpoint = f"{load_balancer_url}/rep"
    add_endpoint = f"{load_balancer_url}/add"
    rm_endpoint = f"{load_balancer_url}/rm"

    asyncio.run(send_requests(10000, load_balancer_url))
    asyncio.run(send_requests_varying_n(10000, load_balancer_url, add_endpoint))
    asyncio.run(test_endpoints(load_balancer_url, rep_endpoint, add_endpoint, rm_endpoint))
