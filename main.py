import time
import requests

from traversal import take_treasure, status_inventory, sell_treasure, wise_explorer, movement, name_changer
from graphutils import bfs
from player import Player

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

header = {"Authorization": f"Token {API_KEY}"}
response = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", headers=header)
player.current_room = response.json()["room_id"]
player.cooldown = response.json()["cooldown"]


## Once we have a name, we no longer collect gold. So I guess this part goes in a while loop. While no name or not 1000 gold, we traverse the map for treasure
while player.gold < 1000 and player.name is "User":

    ## Go to random room
    ## On the way to random room, we need to examine the room each time we enter a new one. So if new room, call function examine
    ## if there are items in the room, then we take those items up until we have 9 items.
    ## When we hit 9 items, we should return to the shop from our current room.
    movement()
    handle_items()
    prev_room = player.current_room


## Go back to the shop and sell the item
path = bfs(player.current_room, 1)
## Try to use wise explorer instead of move endpoint
for m in path:
    room = player.current_room
    exits = map.json[room]["exits"]
    for direction, roomID in exits:
        if roomID == m:
            wise_explorer(direction, API_KEY, roomID )

sell_treasure(player.inventory, API_KEY)


## While 1000 gold, make way to pirate ry.
while player.gold >= 1000:
    path = bfs(player.current_room, 467)
    for m in path:
    room = player.current_room
    exits = map.json[room]["exits"]
    for direction, roomID in exits:
        if roomID == m:
            wise_explorer(direction, API_KEY, roomID)
            
    ## At pirate ry, buy name.
    name_changer(name, API_KEY)

## Go to the shrine, and use pray function


## Move from pirate ry to the well to solve puzzle with ls-8
## Move from the well to the new location
## Mine at new location


def handle_items():
    ## Have to change from map.json? YES
    if len(map.json["items"]) > 0:
        first_response = status_inventory(API_KEY)
        if len(first_response.json()["inventory"]) > 9:
            # change path player.room_id to the shop room_id: 1
            graph.bfs(player.room_id, 1)
        for item in map.json["items"]:
            response = take_treasure(item, API_KEY)
            cooldown = response.json()["cooldown"]
            time.sleep(cooldown)
            break

