import hashlib

class ConsistentHashMap:
    def __init__(self, n_servers=3, n_slots=512, virtual_nodes=9):
        self.n_servers = n_servers
        self.n_slots = n_slots
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.servers = {}

    def add_server(self, server_id):
        for i in range(self.virtual_nodes):
            virtual_id = f"{server_id}#{i}"
            slot = self.hash(virtual_id) % self.n_slots
            self.ring[slot] = server_id
        self.servers[server_id] = set([self.ring[self.hash(f"{server_id}#{i}") % self.n_slots] for i in range(self.virtual_nodes)])

    def remove_server(self, server_id):
        for slot in self.servers[server_id]:
            del self.ring[slot]
        del self.servers[server_id]

    def get_server(self, request_id):
        slot = self.hash(request_id) % self.n_slots
        for i in range(self.n_slots):
            slot_index = (slot + i) % self.n_slots
            if slot_index in self.ring:
                return self.ring[slot_index]
        return None

    @staticmethod
    def hash(data):
        return int(hashlib.sha1(data.encode()).hexdigest(), 16)

    def __str__(self):
        ring_str = "\nConsistent Hash Ring:\n"
        for slot, server_id in sorted(self.ring.items()):
            ring_str += f"Slot {slot}: {server_id}\n"
        return ring_str
