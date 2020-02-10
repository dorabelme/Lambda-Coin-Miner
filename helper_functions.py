import os
from dreamy import dreamy
from cpu import CPU
from mine import proof_of_work, valid_proof
from graphutils import Queue, graph
from dotenv import load_dotenv
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


def handle_items(player, item):
    response = player.take_treasure(item)
    # If boots or jacket have been picked up and are not already being worn, wear them
    if ("boots" in item and not player.footwear) or ("jacket" in item and not player.bodywear):
        player.wear_item(item)

    return response


def status_message(response):
    if "errors" in response and response["errors"]:
        print("\b\b\b ❌ ")
        print(response["errors"])
    else:
        print("\b\b\b ✅ ")
    if TESTING:
        print(response)


def pluralize(word, items):
    if items > 1:
        return f"{word}s"
    else:
        return word


def ls8(description):
    # Extract just the LS-8 program from the message
    code = description[41:].split('\n')

    # Relevant portion of the program that calculates the room number
    #
    # 10000010 LDI R1, VALUE_1      # Load R1 register with VALUE_1
    # 00000001
    # VALUE_1
    # 10000010 LDI R3, VALUE_2      # Load R3 register with VALUE_2
    # 00000010
    # VALUE_2
    # 10101000 AND R1, R3           # Calculate R1 & R3 and store in R1
    # 00000001
    # 00000010
    # 10000010 LDI R3, VALUE_3      # Load R3 register with VALUE_3
    # 00000010
    # VALUE_3
    # 10101011 XOR R1, R3           # Calculate R1 ^ R3 and store in R1
    # 00000001
    # 00000010
    # 01001000 PRA R1               # Print ASCII digit corresponding to the value in R1
    # 00000001
    # 00000001 HLT                  # Halt the CPU

    # Bypass LS-8 emulation by applying equivalent math to extracted values from key locations in the received code
    # PC = 122
    # message = chr(int(f"0b{code[PC]}", 2) & int(
    #     f"0b{code[PC+3]}", 2) ^ int(f"0b{code[PC+9]}", 2))
    # message += chr(int(f"0b{code[PC+17]}", 2) & int(
    #     f"0b{code[PC+20]}", 2) ^ int(f"0b{code[PC+26]}", 2))
    # message += chr(int(f"0b{code[PC+34]}", 2) & int(
    #     f"0b{code[PC+37]}", 2) ^ int(f"0b{code[PC+43]}", 2))

    # Call the LS-8 emulator to run the program
    cpu = CPU()
    cpu.load(code)
    message = cpu.run()[-3:]

    return int(message)


def move_to_location(player, destination, PICKUP_ENABLED=True):
    path = graph.bfs(player.current_room, destination)
    if not path:
        print(f"🤔  Room {player.current_room}? You're already there!")
        return

    optimized_path = [(k, list(g))
                      for k, g in groupby(path, operator.itemgetter(0, 2))]

    distance = len(path)
    moves = len(optimized_path)
    print(
        f"\n🎫  ITINERARY: {distance} {pluralize('room', distance)} in {moves} {pluralize('move', moves)}")
    print("=================================")

    cur_room = player.current_room
    nice_directions = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
    if TESTING:
        print(path, optimized_path)

    count = 1
    for (direction, elevation), rooms in optimized_path:
        destination = rooms[-1][1]

        print(f"{str(count).zfill(2)} ", end="", flush=True)

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
                f"🏃  DASHING {nice_directions[direction]} from room {cur_room} through {next_rooms_nice} to {destination}...", end="", flush=True)

            response = player.dash(direction, len(rooms), next_rooms)
            status_message(response)

        elif elevation != 0 and graph.rooms[destination]['terrain'] != 'CAVE':
            print(
                f"🧚  FLYING {nice_directions[direction]} from room {cur_room} to {destination}...", end="", flush=True)
            response = player.flight(direction)
            print(f"{status_message(response)}  Thank you for flying DreamAir!")

        else:
            print(
                f"🥾  MOVING {nice_directions[direction]} from room {cur_room} to {destination}...", end="", flush=True)
            response = player.wise_explorer(direction, destination)
            status_message(response)

        cur_room = destination
        count += 1

        if PICKUP_ENABLED:
            for item in player.room_items:
                print(f"💰  FOUND {item}! Taking it...", end="", flush=True)
                response = handle_items(player, item)
                status_message(response)
                if "errors" in response and not response["errors"]:
                    print(f"😄  TOOK {item} ✅")

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

    player.current_room = cur_room


def mine(player):
    print(
        f"\n⛏️  MINING for a LambdaCoin...", end="", flush=True)
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
    response = dreamy.post(
        f"{URL}/api/bc/mine/", headers=header, data=data)

    status_message(response)

    # print(response)
    time.sleep(response["cooldown"])
    return response
