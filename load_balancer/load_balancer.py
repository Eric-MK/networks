from flask import Flask, request, jsonify
import json
import random
import requests


# from my_webserver2.consistent_hash import initialize_hash_map, map_request_to_server

from myserver.consistent_hash import initialize_hash_map, map_request_to_server



app = Flask(__name__)

# Simulated list of server containers for demonstration purposes
server_containers = ['Server 1', 'Server 2', 'Server 3']

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(server_containers),
            "replicas": server_containers
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.json
    if not data or 'n' not in data or (data.get('hostnames') and len(data['hostnames']) > data['n']):
        return jsonify({
            "message": "<Error> Invalid request payload",
            "status": "failure"
        }), 400

    num_servers = data['n']
    hostnames = data.get('hostnames')
    
    if hostnames and len(hostnames) != num_servers:
        return jsonify({
            "message": "<Error> Length of hostname list must match the number of new instances",
            "status": "failure"
        }), 400

    if not hostnames:
        # Generate random hostnames if none provided
        hostnames = [f"Server {len(server_containers) + i + 1}" for i in range(num_servers)]

    server_containers.extend(hostnames)
    
    return jsonify({
        "message": {
            "N": len(server_containers),
            "replicas": server_containers
        },
        "status": "successful"
    }), 200

#remove
@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    if not data or 'n' not in data or (data.get('hostnames') and len(data['hostnames']) > data['n']):
        return jsonify({"message": "<Error> Invalid request payload", "status": "failure"}), 400

    num_to_remove = data['n']
    hostnames_to_remove = data.get('hostnames')

    if hostnames_to_remove:
        # Check if all specified hostnames exist
        if not all(hostname in server_containers for hostname in hostnames_to_remove):
            return jsonify({
                "message": "<Error> One or more specified hostnames do not exist",
                "status": "failure"
            }), 400
        if len(hostnames_to_remove) != num_to_remove:
            return jsonify({
                "message": "<Error> Length of hostname list must match the number of instances to be removed",
                "status": "failure"
            }), 400
    else:
        # If no hostnames provided, select random hostnames to remove
        if num_to_remove > len(server_containers):
            return jsonify({"message": "<Error> Trying to remove more instances than available", "status": "failure"}), 400
        hostnames_to_remove = random.sample(server_containers, num_to_remove)

    # Remove the selected hostnames
    for hostname in hostnames_to_remove:
        server_containers.remove(hostname)

    return jsonify({
        "message": {
            "N": len(server_containers),
            "replicas": server_containers
        },
        "status": "successful"
    }), 200


# Initialize the hash map parameters
N = 3  # Number of servers
K = 9  # Number of replicas per server
SLOTS = 512  # Total slots in the hash ring
consistent_hash_map = initialize_hash_map(N, K, SLOTS)
servers = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]  # Base URLs of the server containers



""" @app.route('/<path:path>',methods=['GET'])
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


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
