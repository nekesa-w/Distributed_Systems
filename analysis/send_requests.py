import requests
import random
import json
import time
from collections import defaultdict

def send_requests(base_url, num_requests=1000):
    request_data = defaultdict(int)
    
    for _ in range(num_requests):
        key = str(random.randint(1, 10000))
        response = requests.get(f"{base_url}/{key}")
        if response.status_code == 200:
            server = response.json().get('message', '').split(':')[-1].strip()
            request_data[server] += 1
        time.sleep(0.01)  # Small delay to mimic real-world scenarios
    
    return request_data

if __name__ == "__main__":
    base_url = "http://localhost:5000"
    request_data = send_requests(base_url)
    
    with open('request_data.json', 'w') as f:
        json.dump(request_data, f)
