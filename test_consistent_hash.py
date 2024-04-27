# test_consistent_hash.py
from consistent_hash_map import ConsistentHashMap

# Create a new consistent hash map
chm = ConsistentHashMap()

# Add some servers
chm.add_server("Server_1")
chm.add_server("Server_2")
chm.add_server("Server_3")

# Print the consistent hash ring
print(chm)

# Get the server for a request
request_id = "123456"
server = chm.get_server(request_id)
print(f"Request {request_id} is assigned to {server}")

# Remove a server and check the ring again
chm.remove_server("Server_2")
print(chm)
