import json
import hashlib


def proof_of_work(last_block, difficulty):
    bl_string = json.dumps(last_block, sort_keys=True)
    proof = 0
    while valid_proof(bl_string, proof, difficulty) is False:
        proof += 1
    return proof


def valid_proof(bl_string, proof, difficulty):
    guess = f"{bl_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0" * difficulty
