import hashlib

class ConsistentHash:
    def __init__(self, num_slots=512, virtual_nodes=9):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes
        self.hash_ring = {}
        self.servers = {}

    def add_server(self, server_id):
        for i in range(self.virtual_nodes):
            key = self._hash(f"{server_id}:{i}")
            self.hash_ring[key] = server_id
        self.servers[server_id] = True

    def remove_server(self, server_id):
        for i in range(self.virtual_nodes):
            key = self._hash(f"{server_id}:{i}")
            if key in self.hash_ring:
                del self.hash_ring[key]
        if server_id in self.servers:
            del self.servers[server_id]

    def get_server(self, request_id):
        if not self.hash_ring:
            return None
        key = self._hash(str(request_id))
        for server_key in sorted(self.hash_ring.keys()):
            if server_key >= key:
                return self.hash_ring[server_key]
        return self.hash_ring[min(self.hash_ring.keys())]

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.num_slots

    def hash_request(self, i):
        return (i**2 + 2*i + 17) % self.num_slots

    def hash_server(self, i, j):
        return (i + j + 2*j + 25) % self.num_slots