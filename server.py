import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask
from blockchain import Blockchain

#Instantiate our Node
app = Flask(__name__)

# Generate a globally unique
node_identifier = str(uuid4()).replace('-', '')

# instatiate the blockchian
blockchain = Blockchain()

#@app.route('/mine', methods=['GET'])
#def mine():
    #   return "We'll mine a new Block"

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonfiy(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message' : f"Transaction will be added to Block {index}"}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 블록 채굴에 대한 보상을 설정한다.
    # 송신자를 0으로 표현한 것은 블록 채굴에 대한 보상이기 때문.
    blockchain.new_transaction(
        sender="0", recipient=node_identifier, amount = 1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message' : "New Block Forged",
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['prevoous_hash'],
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
