import requests
import time

def test_failure_recovery():
    initial_servers = requests.get("http://localhost:5000/rep").json()['message']['replicas']
    
    start_time = time.time()
    response = requests.post("http://localhost:5000/simulate_failure", json={"server": initial_servers[0]})
    recovery_time = response.json()['recovery_time']
    
    new_servers = requests.get("http://localhost:5000/rep").json()['message']['replicas']
    
    print(f"Initial servers: {initial_servers}")
    print(f"New servers: {new_servers}")
    print(f"Recovery time: {recovery_time} seconds")

if __name__ == "__main__":
    test_failure_recovery()