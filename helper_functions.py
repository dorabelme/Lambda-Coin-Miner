import os
from dreamy import dreamy
from mine import proof_of_work, valid_proof
from graphutils import Queue, graph
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
    # path = graph.bfs(player.current_room, 0)
    print(path)
    distance = len(path)
    print(f"{distance} steps away from your destination")
    if distance == 0:
        return

    plan = [path[0]]
    for i in range(1, len(path)):
        # print(plan)
        prev_dir, prev_id, prev_elev = path[i - 1]
        cur_dir, cur_id, cur_elev = path[i]

        if cur_dir != prev_dir or cur_elev > prev_elev:
            if len(plan) > 1:
                room_list = ','.join([str(room[1]) for room in plan])
                print(
                    f"Dashing {prev_dir} from room {player.current_room} to room {plan[-1][1]}")
                print(f"Next rooms: {room_list}")
                # Call dash
                response = player.dash(prev_dir, len(plan), room_list)
                print(response)
                plan = [path[i]]
            else:
                print(
                    f"Moving {prev_dir} from room {player.current_room} to room {plan[0][1]}")
                response = player.wise_explorer(prev_dir, plan[0][1])
                print(response)
                plan = [path[i]]
        else:
            plan.append(path[i])
        prev_dir, prev_id, prev_elev = cur_dir, cur_id, cur_elev

    distance = len(plan)
    for m in plan:
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
        cooldown = response["cooldown"]
        time.sleep(cooldown)
        if "errors" in response and response["errors"]:
            print(response["errors"])


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
