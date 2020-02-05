import json
import hashlib

DIFFICULTY = 6

def proof_of_work(last_block):
    bl_string = json.dumps(last_block, sort_keys=True)
    proof = 0
    while valid_proof(bl_string, proof) is False:
        proof += 1
    return proof

def valid_proof(bl_string, proof):
    guess = f"{bl_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY