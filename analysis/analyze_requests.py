import json
import matplotlib.pyplot as plt

def load_request_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_distribution(request_data):
    servers = list(request_data.keys())
    request_counts = list(request_data.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, request_counts, color='skyblue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Load Distribution Among Servers')
    plt.xticks(rotation=45)
    plt.show()

def plot_pie_chart(request_data):
    servers = list(request_data.keys())
    request_counts = list(request_data.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(request_counts, labels=servers, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Load Distribution Among Servers')
    plt.show()

if __name__ == "__main__":
    request_data = load_request_data('request_data.json')
    plot_distribution(request_data)
    plot_pie_chart(request_data)
