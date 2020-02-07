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

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL

player = Player()

from itertools import groupby
import operator

# path = [('warp', 765, 0), ('e', 693, 0), ('e', 640, 0), ('n', 607, 0), ('w', 630, 0), ('w', 755, 0), ('w', 766, 0), ('s', 931, 0), ('warp', 431, 0), ('w', 492, 0)]
path=[('s', 249, 0), ('s', 240, 0), ('w', 221, 0), ('w', 184, 0), ('w', 127, 0), ('w', 120, 0), ('n', 107, 0), ('w', 104, 0), ('n', 59, 0), ('n', 38, 0), ('w', 33, 0), ('w', 31, 0), ('n', 30, 0), ('w', 27, 0), ('w', 20, 0), ('s', 19, 0), ('s', 10, 0), ('s', 0, 0), ('s', 2, 0), ('e', 3, 1), ('s', 9, 2), ('s', 12, 3), ('s', 18, 4), ('s', 22, 5), ('s', 78, 4), ('s', 108, 3), ('s', 117, 2), ('s', 131, 1), ('w', 138, 0), ('w', 195, 0), ('s', 228, 0), ('s', 281, 0), ('w', 317, 0), ('s', 387, 0), ('w', 431, 0), ('w', 492, 0)]

optimized_path = [(k,list(g)) for k, g in groupby(path, operator.itemgetter(0,2))]

prev_elev = None
cur_room = 0
for (direction, elevation), rooms in optimized:
  # print(direction, rooms)
  last_room = rooms[-1][1]
  if len(rooms) > 1:
    print(f"Dashing {direction} from room {cur_room} to {last_room}")
  elif elevation != prev_elev:
    print(f"Flying {direction} from room {cur_room} to {last_room}")
  else:
    print(f"Moving {direction} from room {cur_room} to {last_room}")
  prev_elev, cur_room = elevation, last_room
  
  

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
