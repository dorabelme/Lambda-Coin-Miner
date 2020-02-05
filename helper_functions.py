from dreamy import dreamy
from mine import proof_of_work, valid_proof
from graphutils import Queue

def handle_items(player, item):
    player.take_treasure(item)
    # If boots or jacket have been picked up and are not already being worn, wear them
    if ("boots" in item and not player.footwear) or ("jacket" in item and not player.bodywear):
        player.wear_item(item)


def move_to_location(player, path):
    # queue = Queue()
    # prev_dir = None
    # for m in path:
        
    distance = len(path)
    for m in path:
        print(f"{distance} steps away from your destination")
        player.wise_explorer(m[0], m[1])
        # player.movement(m[0])
        print(f"Moving {m[0]} to room {m[1]}")
        distance -= 1
        # cooldown = response["cooldown"]
        # time.sleep(cooldown)
        # if "errors" in response:
        #     print(response["errors"])

def mine(player):
        header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
        }
        response = dreamy.get(
        f"{URL}/api/bc/last_proof/", headers=header)
        last_bl = response["proof"]
        new_proof = proof_of_work(last_bl)
        data = {"proof": new_proof}
        response = dreamy.post(
        f"{URL}/api/bc/mine/", headers=header, data=data)
        print(response)