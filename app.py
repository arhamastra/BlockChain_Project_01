import hashlib
import json
from time import time
from typing import List, Dict
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new Block and adds it to the chain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, product_data):
        """
        Adds a new transaction to the list of transactions
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'product_data': product_data
        })
        return self.last_block['index'] + 1

    def hash(self, block):
        """
        Hashes a Block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def proof_of_work(last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes
        - Where p is the previous proof, and p' is the new proof
        """
        proof = 0
        while Blockchain.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain leading 4 zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        return self.chain[-1]

    def get_chain(self):
        """
        Returns the full blockchain
        """
        return self.chain

    def is_valid(self):
        """
        Validates the entire blockchain
        """
        last_block = self.chain[0]
        current_index = 1
        while current_index < len(self.chain):
            block = self.chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not Blockchain.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

app = Flask(__name__, static_folder='static')
CORS(app) 

blockchain = Blockchain()

@app.route('/')
def index():
    """
    Serve the main HTML interface
    """
    return send_from_directory('static', 'index.html')

@app.route('/api')
def api_home():
    """
    API information endpoint
    """
    return jsonify({
        'message': 'Blockchain API is running',
        'version': '1.0.0',
        'endpoints': {
            '/': 'GET - Web Interface',
            '/api': 'GET - API Information',
            '/api/transaction/new': 'POST - Create new transaction',
            '/api/mine': 'GET - Mine a new block',
            '/api/chain': 'GET - Get full blockchain',
            '/api/validate': 'GET - Validate blockchain'
        }
    }), 200

@app.route('/api/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required_fields = ['sender', 'recipient', 'product_data']
    if not all(field in values for field in required_fields):
        return jsonify({'error': 'Missing values', 'required': required_fields}), 400

    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['product_data']
    )
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/api/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient="miner_address",
        product_data="Mining reward"
    )
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/api/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.get_chain(),
        'length': len(blockchain.get_chain())
    }
    return jsonify(response), 200

@app.route('/api/validate', methods=['GET'])
def validate_chain():
    if blockchain.is_valid():
        return jsonify({'message': 'Blockchain is valid', 'valid': True}), 200
    else:
        return jsonify({'message': 'Blockchain is not valid', 'valid': False}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
