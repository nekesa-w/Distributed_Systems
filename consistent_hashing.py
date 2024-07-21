# consistent_hashing.py

import hashlib

class ConsistentHash:
    def __init__(self, num_slots=512, num_virtual_nodes=9):
        self.num_slots = num_slots
        self.num_virtual_nodes = num_virtual_nodes
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        for i in range(self.num_virtual_nodes):
            virtual_node_id = f"{server_id}-{i}"
            hash_key = self._hash(virtual_node_id)
            self.ring[hash_key] = server_id
            self.sorted_keys.append(hash_key)
        self.sorted_keys.sort()

    def remove_server(self, server_id):
        for i in range(self.num_virtual_nodes):
            virtual_node_id = f"{server_id}-{i}"
            hash_key = self._hash(virtual_node_id)
            del self.ring[hash_key]
            self.sorted_keys.remove(hash_key)

    def get_server(self, key):
        hash_key = self._hash(key)
        for k in self.sorted_keys:
            if hash_key <= k:
                return self.ring[k]
        return self.ring[self.sorted_keys[0]]
