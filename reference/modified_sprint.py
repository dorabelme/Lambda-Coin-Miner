import os
from os.path import join, dirname
from dotenv import load_dotenv
from util import Graph
import requests
import time
import json
import random

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

travels_log = open("./travels_log.txt", "a+")
items_log = open("./items.json", "a+")

found_items = set()
wearing_boots = False
wearing_jacket = False

api_key = os.environ.get("API_KEY")
# base_url = "https://treasure-hunt-test.herokuapp.com/api/adv"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
headers = {"Authorization": f"Token {api_key}"}

graph = Graph()
r = requests.get(f"{base_url}/init/", headers=headers).json()
print(r)
print(f"Starting room: {r['room_id']}")
time.sleep(15)

travels_log.write(json.dumps(r) + ",")

player = {}
player_current_room = graph.add_room(r)

# Seed for the pseudorandom number generator
seed = 386839

# Seed the random number generator for reproducible results
random.seed(seed)

# Will be filled with directions to walk
traversal_path = []

# Keep track of visited rooms so we know when we've visited them all
visited_rooms = set()
visited_rooms.add(player_current_room["room_id"])

backtracked = False  # Track whether player has returned from a dead end

player_current_room["cooldown"] = 15

# Loop until all rooms have been visited
while len(visited_rooms) != 500:
    travels_log.flush()
    items_log.flush()
    print(f"Rooms visited: {len(visited_rooms)}")
    # Look for and log items in the current room
    # Get boots or jacket and wear them if we haven't already
    for item in player_current_room["items"]:
        if item not in found_items:
            found_items.add(item)
            try:
                i = requests.post(f"{base_url}/examine/", headers=headers,
                                  data=json.dumps({"name": item})).json()
            except Exception as e:
                print(f"Error: {e}")

            print(f"New item found: {item}")
            print(i)
            items_log.write(json.dumps(i) + ",")
            time.sleep(i["cooldown"])
            if not wearing_boots and "boots" in item:
                i = requests.post(f"{base_url}/take/", headers=headers,
                                  data=json.dumps({"name": item})).json()
                print(f"Took: {item}")
                time.sleep(i["cooldown"])
                i = requests.post(f"{base_url}/wear/", headers=headers,
                                  data=json.dumps({"name": item})).json()
                print(f"Wearing: {item}")
                wearing_boots = True
                time.sleep(i["cooldown"])
            elif not wearing_jacket and "jacket" in item:
                i = requests.post(f"{base_url}/take/", headers=headers,
                                  data=json.dumps({"name": item})).json()
                print(f"Took: {item}")
                time.sleep(i["cooldown"])
                i = requests.post(f"{base_url}/wear/", headers=headers,
                                  data=json.dumps({"name": item})).json()
                print(f"Wearing: {item}")
                wearing_jacket = True
                time.sleep(i["cooldown"])

    # Get a list of unvisited exits from the current location
    exits = graph.get_connected_rooms(
        player_current_room["room_id"], visited=False)

    # If there are exits
    if exits:
        # Store current room for connecting to the next room
        current_room = player_current_room

        # If we didn't backtrack, bias toward making turns rather than going straight
        if not backtracked:
            # If there's more than one exit, remove the direction player came from
            # In order to force a turn
            if len(exits) > 1 and len(traversal_path) > 0:
                prev_dir = traversal_path[-1]
                # 30% of the time, don't continue straight
                if prev_dir in exits and random.random() > 0.7:
                    exits.remove(prev_dir)
                direction = random.choice(exits)
            else:
                direction = exits[0]
        else:
            # If we backtracked from a dead end, take next avail clockwise turn
            direction = exits[0]
            backtracked = False

        print(f"Direction: {direction}")
        try:
            r = requests.post(f"{base_url}/move/", headers=headers,
                              data=json.dumps({"direction": direction})).json()
        except Exception as e:
            print(f"Error: {e}")

        travels_log.write(json.dumps(r) + ",")

        if "room_id" not in r:
            print(f"Error: {r}")
        else:
            player_current_room = graph.get_room(r["room_id"])
            if not player_current_room:
                player_current_room = graph.add_room(r)

            traversal_path.append(direction)

            visited_rooms.add(player_current_room["room_id"])
            graph.connect_rooms(
                current_room["room_id"], player_current_room["room_id"], direction)

        player_current_room["cooldown"] = r["cooldown"]
        time.sleep(player_current_room["cooldown"])

    else:
        route = graph.explore_bfs(player_current_room["room_id"])
        for direction in route:
            print(f"Direction: {direction}")
            try:
                r = requests.post(f"{base_url}/move/", headers=headers,
                                  data=json.dumps({"direction": direction, "next_room_id": str(player_current_room["exits"][direction])})).json()
            except Exception as e:
                print(f"Error: {e}")

            print(r)
            player_current_room = graph.get_room(r["room_id"])
            traversal_path.append(direction)
            player_current_room["cooldown"] = r["cooldown"]
            time.sleep(player_current_room["cooldown"])
        backtracked = True
    print()

travels_log.write("]")
travels_log.close()

items_log.write("]")
items_log.close()


# TRAVERSAL TEST
# visited_rooms = set()
# player_current_room = world.starting_room
# visited_rooms.add(player_current_room["room_id"])

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player_current_room["room_id"])

# if len(visited_rooms) == len(room_graph):
#     print(
#         f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
# print(f"TOTAL MOVES: {len(traversal_path)}")

world_map = open("./worldmap.json", "w")
world_map.write(json.dumps(graph.rooms))
world_map.close()
