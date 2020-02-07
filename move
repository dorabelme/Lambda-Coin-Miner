#!/usr/bin/env python

import os
import sys
from dreamy import dreamy
from mine import proof_of_work, valid_proof
from graphutils import graph, Queue
from dotenv import load_dotenv
from player import Player
from itertools import groupby
import operator
import time

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL

player = Player()


def handle_items(item):
    response = player.take_treasure(item)
    # If boots or jacket have been picked up and are not already being worn, wear them
    if ("boots" in item and not player.footwear) or ("jacket" in item and not player.bodywear):
        player.wear_item(item)

    return response


def status_message(response):
    if "errors" in response and response["errors"]:
        print("\b\b\b ❌")
        print(response["errors"])
    else:
        print("\b\b\b ✅")
    if TESTING:
        print(response)


def pluralize(word, items):
    if items > 1:
        return f"{word}s"
    else:
        return word


def move_to_location(destination):
    print(player.current_room, destination)
    path = graph.bfs(player.current_room, destination)
    optimized_path = [(k, list(g))
                      for k, g in groupby(path, operator.itemgetter(0, 2))]

    distance = len(path)
    if distance == 0:
        print("Room {player.current_room}? You're already there!")
        return

    moves = len(optimized_path)
    print(
        f"\n🎫  ITINERARY: {distance} {pluralize('room', distance)} in {moves} {pluralize('move', moves)}")
    print("=================================")

    prev_elev = None
    cur_room = player.current_room
    nice_directions = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
    if TESTING:
        print(path, optimized_path)
    for (direction, elevation), rooms in optimized_path:
        destination = rooms[-1][1]

        if direction == "warp":
            print(
                f"✨  WARPING from room {cur_room} to {destination}...", end="", flush=True)
            response = player.warp()
            status_message(response)

        elif direction == "recall":
            print(
                f"🏠  RECALLING from room {cur_room} to 0...", end="", flush=True)
            response = player.recall()
            status_message(response)

        elif len(rooms) > 1:
            next_rooms = ','.join([str(room[1]) for room in rooms])
            next_rooms_nice = ','.join([str(room[1]) for room in rooms[:-1]])
            print(
                f"🏃  DASHING {nice_directions[direction]} from room {cur_room} through [{next_rooms_nice}] to {destination}...", end="", flush=True)

            response = player.dash(direction, len(rooms), next_rooms)
            status_message(response)

        elif elevation != 0 and graph.rooms[destination]['terrain'] != 'CAVE':
            print(
                f"🧚  FLYING {nice_directions[direction]} from room {cur_room} to {destination}...", end="", flush=True)
            response = player.flight(direction)
            print(f"{status_message(response)} Thank you for flying DreamAir!")

        else:
            print(
                f"🥾  MOVING {nice_directions[direction]} from room {cur_room} to {destination}...", end="", flush=True)
            response = player.wise_explorer(direction, destination)
            status_message(response)

        prev_elev, cur_room = elevation, destination

        if player.encumbrance < player.strength - 1 and player.room_items:
            item = player.room_items[0]
            print(f"💰  FOUND {item}! Taking it...", end="", flush=True)
            response = handle_items(item)
            status_message(response)
            if "errors" in response and not response["errors"]:
                print(f"😄  TOOK {item}")
                print(f"🎒  INVENTORY: {', '.join(player.inventory)}")

        cooldown = response["cooldown"]
        time.sleep(cooldown)
        if "errors" in response and response["errors"]:
            print(response["errors"])

    print()
    for field in ["Description", "Terrain", "Elevation", "Players", "Items", "Cooldown"]:
        if field.lower() in response:
            val = response[field.lower()]
            if val:
                print(f"{field.upper()}: ", end="", flush=True)
                if not isinstance(val, list):
                    print(val)
                else:
                    if field == "Players":
                        values = "👤  " + " 👤  ".join(val)
                    else:
                        values = ", ".join(val)
                    print(values)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        move_to_location(int(sys.argv[1]))
    else:
        print(f"Usage: {sys.argv[0]} <destination room id>")
