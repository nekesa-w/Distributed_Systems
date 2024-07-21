import math

class ServerContainer:
    def __init__(self, id):
        self.id = id
        self.virtual_servers = []

class ConsistentHashMap:
    def __init__(self, num_containers, num_slots):
        self.num_containers = num_containers
        self.num_slots = num_slots
        self.containers = [ServerContainer(i) for i in range(num_containers)]
        self.hash_map = [None] * num_slots

    def hash_request(self, request_id):
        """Hash function for mapping requests to slots."""
        return (request_id + 2 * request_id + 17) % self.num_slots

    def hash_virtual_server(self, container_id, replica_id):
        """Hash function for mapping virtual servers to slots."""
        return (container_id + replica_id + 2 * replica_id + 25) % self.num_slots

    def add_virtual_servers(self):
        """Add virtual servers for each container to the hash map."""
        num_virtual_servers = math.ceil(math.log2(self.num_slots))
        for container in self.containers:
            for j in range(num_virtual_servers):
                slot = self.hash_virtual_server(container.id, j)
                container.virtual_servers.append(slot)
                
                # Handle collision using linear probing
                if self.hash_map[slot] is None:
                    self.hash_map[slot] = container
                else:
                    next_slot = (slot + 1) % self.num_slots
                    while self.hash_map[next_slot] is not None:
                        next_slot = (next_slot + 1) % self.num_slots
                    self.hash_map[next_slot] = container

    def map_request_to_container(self, request_id):
        """Map a request ID to a server container."""
        slot = self.hash_request(request_id)
        container = self.hash_map[slot]
        if container is None:
            return None  # No server container found for this request
        else:
            return container.id

# Initialize consistent hash map
num_containers = 3
num_slots = 512
consistent_hash_map = ConsistentHashMap(num_containers, num_slots)

# Add virtual servers to the hash map
consistent_hash_map.add_virtual_servers()

# Map requests to server containers
request_id = 23567
container_id = consistent_hash_map.map_request_to_container(request_id)
print("Request", request_id, "is mapped to Server Container", container_id)