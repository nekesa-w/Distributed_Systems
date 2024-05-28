import hashlib
import bisect
import math

class ConsistentHashMap:
    def __init__(self, num_servers=3, num_slots=512, num_virtual_servers=None):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers if num_virtual_servers else int(math.log2(num_slots))
        self.ring = []
        self.nodes = {}
        
        self._initialize_servers()

    def _hash_request(self, request_id):
        return (request_id + 2 * request_id**2 + 17) % self.num_slots

    def _hash_virtual_server(self, server_id, replica_id):
        return (server_id + replica_id + 2 * replica_id**2 + 25) % self.num_slots

    def _initialize_servers(self):
        for server_id in range(1, self.num_servers + 1):
            for replica_id in range(self.num_virtual_servers):
                slot = self._hash_virtual_server(server_id, replica_id)
                self._add_to_ring(slot, server_id)

    def _add_to_ring(self, slot, server_id):
        if slot in self.nodes:
            # Handle collision with quadratic probing
            i = 1
            while slot in self.nodes:
                slot = (slot + i**2) % self.num_slots
                i += 1
        bisect.insort(self.ring, slot)
        self.nodes[slot] = server_id

    def get_server(self, request_id):
        if not self.ring:
            return None
        slot = self._hash_request(request_id)
        idx = bisect.bisect(self.ring, slot)
        if idx == len(self.ring):
            idx = 0
        return self.nodes[self.ring[idx]]

    def add_server(self, new_server_id):
        for replica_id in range(self.num_virtual_servers):
            slot = self._hash_virtual_server(new_server_id, replica_id)
            self._add_to_ring(slot, new_server_id)

    def remove_server(self, server_id):
        to_remove = [slot for slot, sid in self.nodes.items() if sid == server_id]
        for slot in to_remove:
            self.ring.remove(slot)
            del self.nodes[slot]

# Example usage
hash_map = ConsistentHashMap(num_servers=3)

print("Initial Mapping:")
for request_id in [132574, 287430, 549321]:
    server = hash_map.get_server(request_id)
    print(f"Request {request_id} is mapped to Server {server}")

print("\nAdding a new server:")
hash_map.add_server(4)
for request_id in [132574, 287430, 549321]:
    server = hash_map.get_server(request_id)
    print(f"Request {request_id} is mapped to Server {server}")

print("\nRemoving a server:")
hash_map.remove_server(2)
for request_id in [132574, 287430, 549321]:
    server = hash_map.get_server(request_id)
    print(f"Request {request_id} is mapped to Server {server}")

