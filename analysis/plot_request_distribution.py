import matplotlib.pyplot as plt
import requests

def plot_request_distribution():
    stats = requests.get("http://localhost:5000/stats").json()
    
    servers = list(stats.keys())
    counts = list(stats.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, counts)
    plt.title("Request Distribution Across Servers")
    plt.xlabel("Server ID")
    plt.ylabel("Number of Requests")
    plt.savefig("request_distribution.png")
    plt.close()

if __name__ == "__main__":
    plot_request_distribution()