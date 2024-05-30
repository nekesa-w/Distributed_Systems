import requests
import matplotlib.pyplot as plt

def send_requests():
    server_counts = {'Server 1': 0, 'Server 2': 0, 'Server 3': 0}
    for _ in range(10000):
        response = requests.get('http://localhost:5000/home') 
        server_id = response.json()['message'].split(': ')[1]
        server_counts[server_id] += 1
    return server_counts

def plot_bar_chart(server_counts):
    servers = list(server_counts.keys())
    counts = list(server_counts.values())
    plt.bar(servers, counts)
    plt.xlabel('Server')
    plt.ylabel('Request Count')
    plt.title('Request Distribution Among Server Containers')
    plt.show()

if __name__ == '__main__':
    counts = send_requests()
    print(counts)
    plot_bar_chart(counts)
