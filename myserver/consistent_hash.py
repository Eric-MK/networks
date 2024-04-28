# hash map logic

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

N = 3
K = 9
SLOTS = 512
consistent_hash_map = initialize_hash_map(N, K, SLOTS)


