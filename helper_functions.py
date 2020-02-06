import os
from dreamy import dreamy
from mine import proof_of_work, valid_proof
from graphutils import Queue
from dotenv import load_dotenv
import time

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL


def handle_items(player, item):
    player.take_treasure(item)
    # If boots or jacket have been picked up and are not already being worn, wear them
    if ("boots" in item and not player.footwear) or ("jacket" in item and not player.bodywear):
        player.wear_item(item)


def move_to_location(player, path):
    count = 1
    plan = [path[0]]
    for i in range(1, len(path)):
        prev_dir, prev_id, prev_elev = path[i - 1]
        cur_dir, cur_id, cur_elev = path[i]

        # If done collecting dash rooms
        if cur_dir != prev_dir and len(plan) > 1:
            # Then Dash
            room_list = ','.join([str(room[1]) for room in plan])
            print(
                f"Dashing {plan[0][0]} from room {plan[0][1]} to room {plan[-1][1]}")
            print(f"Rooms: {room_list}")
            # Call dash
            plan = []
            count = 1
        elif cur_dir == prev_dir:
            plan.append(path[i])
            count += 1

    distance = len(path)
    for m in path:
        print(f"{distance} steps away from your destination")
        print(f"Moving {m[0]} to room {m[1]}")
        response = player.wise_explorer(m[0], m[1])
        # Check for fields in response and output values if present
        for field in ["Description", "Terrain", "Elevation", "Players", "Items", "Cooldown"]:
            if field.lower() in response:
                val = response[field.lower()]
                print(f"{field.upper()}: ", end="")
                if not isinstance(val, list):
                    print(val)
                else:
                    print(*val, sep=", ")
        print()
        distance -= 1
        if player.encumbrance < player.strength - 1 and player.room_items:
            item = player.room_items[0]
            print(f"Found {item}! Taking it...")
            handle_items(player, item)
            print(f"Took {item}.\nCurrent items: {player.inventory}")
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
    difficulty = response["difficulty"]
    new_proof = proof_of_work(last_bl, difficulty)
    data = {"proof": new_proof}
    print(f"Submitting proof: {new_proof}")
    response = dreamy.post(
        f"{URL}/api/bc/mine/", headers=header, data=data)

    # print(response)
    time.sleep(response["cooldown"])
    return response
