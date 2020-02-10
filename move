#!/usr/bin/env python

import sys
from player import Player
from helper_functions import move_to_location


if __name__ == '__main__':
    if len(sys.argv) > 1:
        player = Player()
        PICKUP_ENABLED = True if len(sys.argv) == 3 else False
        move_to_location(player, int(sys.argv[1]), PICKUP_ENABLED)
    else:
        print(f"Usage: {sys.argv[0]} <destination room id> pickup")
