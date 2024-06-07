
"""

#define the hash functions
def request_hash(i):
    return (i + 2 * i**2 + 17) % 512

def virtual_server_hash(i, j):
    return (i + j + 2 * j**2 + 25) % 512


#create the consistent hash map
def initialize_hash_map(n, k, slots):
    hash_map = [None] * slots
    for i in range(n):
        for j in range(k):
            slot = virtual_server_hash(i, j)
            # Implementing linear probing to resolve collisions
            while hash_map[slot] is not None:
                slot = (slot + 1) % slots #assign server container ID to the slot
            hash_map[slot] = i
    return hash_map


#Map requaests to the hash map
def map_request_to_server(request_id, hash_map):
    slot = request_hash(request_id)
    server_id = hash_map[slot]
    if server_id is None:
        #Implement linear probing for unassigned slots
        original_slot = slot
        while hash_map[slot] is None:
            slot = (slot + 1) % 512
            if slot == original_slot:
                raise Exception("No available server found, hash map is full")
    return hash_map[slot]

# Initialize the hash map parameters
N = 3  # Number of servers
K = 9  # Number of replicas per server
SLOTS = 512  # Total slots in the hash ring
consistent_hash_map = initialize_hash_map(N, K, SLOTS)
servers = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]  # Base URLs of the server containers



 @app.route('/<path:path>',methods=['GET'])
def proxy_request(path):
    try:
        # Convert incoming path to a unique integer hash code, you might need to adjust logic based on actual path usage
        request_id = hash(path)
        # Map this request ID to a server using your consistent hash map
        server_index = map_request_to_server(request_id, consistent_hash_map)
        target_server = servers[server_index]
        # Forward the request to the correct server and retrieve the response
        response = requests.get(f"{target_server}/{path}")
        if response.status_code == 404:
            return jsonify({"message": f"Error: '/{path}' endpoint does not exist in server replicas", "status": "failure"}), 400
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"message": str(e), "status": "failure"}), 500
"""
