import subprocess
import requests
import matplotlib.pyplot as plt

def run_experiment(num_servers, num_requests):
    requests.post("http://localhost:5000/add", json={"n": num_servers})
    
    subprocess.run(["python", "client.py", str(num_requests)])
    
    stats = requests.get("http://localhost:5000/stats").json()
    return sum(stats.values()) / len(stats)

def main():
    results = []
    for n in range(2, 7):
        avg_load = run_experiment(n, 10000)
        results.append((n, avg_load))
    
    servers, loads = zip(*results)
    plt.plot(servers, loads, marker='o')
    plt.title("Average Server Load vs Number of Servers")
    plt.xlabel("Number of Servers")
    plt.ylabel("Average Load per Server")
    plt.savefig("scalability_analysis.png")
    plt.close()

if __name__ == "__main__":
    main()