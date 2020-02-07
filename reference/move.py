#!/usr/bin/env python

import os
import sys
from dreamy import dreamy
from mine import proof_of_work, valid_proof
from graphutils import graph, Queue
from dotenv import load_dotenv
from player import Player

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL

player = Player()


def move_to_location(destination):
    print(player.current_room, destination)
    path = graph.bfs(player.current_room, destination)
    print(path)
    if path:
        distance = len(path)
        for m in path:
            print(f"{distance} steps away from your destination")
            player.wise_explorer(m[0], m[1])
            # player.movement(m[0])
            print(f"Moving {m[0]} to room {m[1]}")
            distance -= 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        move_to_location(int(sys.argv[1]))
    else:
        print(f"Usage: {sys.argv[0]} <destination room id>")
