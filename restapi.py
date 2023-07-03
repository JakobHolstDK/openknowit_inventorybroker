from flask import Flask, jsonify, request
from pymongo import MongoClient
import libvirt
import os

mongoserver = os.getenv("MONGO")


app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://prodmongo001.openknowit.com:27017/')
try:
  db = client['kvm_db']
  connections_collection = db['connections']
except:
    print("Error connection to mongo at %s" % mongoserver)
    exit(1)
    

@app.route('/kvm/connection', methods=['POST'])
def create_kvm_connection():
    # Get the connection details from the request body
    connection_info = request.get_json()
    uri = connection_info['uri']
    
    try:
        # Create a KVM connection
        conn = libvirt.open(uri)
        
        # Store the connection information in MongoDB
        connection_id = connections_collection.insert_one({
            'uri': uri
        }).inserted_id
        
        return jsonify({'message': 'KVM connection created', 'connection_id': str(connection_id)}), 201
    
    except libvirt.libvirtError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()

