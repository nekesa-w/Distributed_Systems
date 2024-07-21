import requests
import matplotlib.pyplot as plt
import numpy as np
import time

BASE_URL = "http://localhost:5000"

def launch_async_requests(num_requests):
    responses = []
    for i in range(num_requests):
        response = requests.get(f"{BASE_URL}/home")
        responses.append(response.json())
    return responses

def analyze_requests(responses):
    server_counts = {}
    for response in responses:
        server_id = response['message'].split(": ")[-1]
        if server_id in server_counts:
            server_counts[server_id] += 1
        else:
            server_counts[server_id] = 1
    return server_counts

def plot_bar_chart(server_counts):
    servers = list(server_counts.keys())
    counts = list(server_counts.values())
    
    plt.bar(servers, counts)
    plt.xlabel('Server ID')
    plt.ylabel('Number of Requests')
    plt.title('Requests Handled by Each Server')
    plt.show()

def increment_servers_and_test():
    server_loads = []
    for n in range(2, 7):  # Increment N from 2 to 6
        # Add servers
        requests.post(f"{BASE_URL}/add", json={"n": n, "hostnames": [f"Server {i+1}" for i in range(n)]})
        
        # Launch requests
        responses = launch_async_requests(10000)
        server_counts = analyze_requests(responses)
        
        # Calculate average load
        average_load = sum(server_counts.values()) / n
        server_loads.append(average_load)
        
        # Remove servers after testing
        requests.delete(f"{BASE_URL}/rm", json={"n": n, "hostnames": [f"Server {i+1}" for i in range(n)]})
    
    return server_loads

def plot_line_chart(server_loads):
    x = np.arange(2, 7)
    plt.plot(x, server_loads, marker='o')
    plt.xlabel('Number of Servers (N)')
    plt.ylabel('Average Load per Server')
    plt.title('Average Load Distribution with Increasing Servers')
    plt.xticks(x)
    plt.grid()
    plt.show()

def test_server_failure():
    # Simulate server failure by removing one server
    response = requests.get(f"{BASE_URL}/rep")
    replicas = response.json()['replicas']
    
    if len(replicas) > 0:
        server_to_remove = replicas[0]
        requests.delete(f"{BASE_URL}/rm", json={"n": 1, "hostnames": [server_to_remove]})
        print(f"Removed server: {server_to_remove}")

        # Launch requests to see if load balancer spawns a new instance
        responses = launch_async_requests(10000)
        server_counts = analyze_requests(responses)
        print(f"Requests after failure: {server_counts}")

def main():
    # Task A-1: Launch 10,000 async requests
    responses = launch_async_requests(10000)
    server_counts = analyze_requests(responses)
    plot_bar_chart(server_counts)

    # Task A-2: Increment servers and test
    server_loads = increment_servers_and_test()
    plot_line_chart(server_loads)

    # Task A-3: Test server failure
    test_server_failure()

if __name__ == "__main__":
    main()