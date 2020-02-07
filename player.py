from dotenv import load_dotenv
from dreamy import dreamy
import os
import time

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL


class Player:
    def __init__(self):
        # Get current room and cooldown
        self.init_player()

        # Get player stats
        self.status_update()

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def init_player(self):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.get(
            f"{URL}/api/adv/init/",
            headers=header
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        self.cooldown = response["cooldown"]

        time.sleep(self.cooldown)
        return response

    def status_update(self):
        # print(f"Status update. Cooldown: {self.cooldown}")
        time.sleep(self.cooldown)
        status_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/status/",
            headers=status_header,
            cooldown=self.cooldown
        )

        self.name = response["name"]
        # self.cooldown = response["cooldown"]
        self.encumbrance = response["encumbrance"]
        self.strength = response["strength"]
        self.speed = response["speed"]
        self.gold = response["gold"]

        if not TESTING:
            self.bodywear = response["bodywear"]
            self.footwear = response["footwear"]
            self.abilities = response["abilities"]
        else:
            self.bodywear = None
            self.footwear = None
            self.abilities = []

        self.inventory = response["inventory"]
        self.status = response["status"]
        self.errors = response["errors"]
        self.messages = response["messages"]

        time.sleep(self.cooldown)
        # print(self.cooldown)
        return response

    def movement(self, direction):
        movement_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/move/",
            headers=movement_header,
            data={"direction": direction},
            cooldown=self.cooldown
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        self.cooldown = response["cooldown"]

        time.sleep(self.cooldown)
        return response

    def wise_explorer(self, direction, room_id):
        movement_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }

        response = dreamy.post(
            f"{URL}/api/adv/move/",
            headers=movement_header,
            data={"direction": direction, "next_room_id": str(room_id)},
            cooldown=self.cooldown
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        self.cooldown = response["cooldown"]

        time.sleep(self.cooldown)
        return response

    def take_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/take/",
            headers=treasure_header,
            data={"name": f"{treasure}"},
            cooldown=self.cooldown
        )

        time.sleep(self.cooldown)
        self.status_update()
        return response

    def drop_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/drop/",
            headers=treasure_header,
            data={"name": f"{treasure}"},
            cooldown=self.cooldown
        )

        self.status_update()
        return response

    def sell_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/sell/",
            headers=treasure_header,
            data={"name": f"{treasure}", "confirm": "yes"},
            cooldown=self.cooldown
        )

        time.sleep(self.cooldown)
        self.status_update()
        return response

    def examine(self, treasure, player=None):
        inventory_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/examine/",
            headers=inventory_header,
            data={"name": f"{treasure or player}"},
            cooldown=self.cooldown
        )
        return response

    def balance(self):
        balance_header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.get(
            f"{URL}/api/bc/get_balance/",
            headers=balance_header,
            cooldown=self.cooldown
        )

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        self.status_update()
        return response

    def name_changer(self, name):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/change_name/",
            headers=header,
            data={"name": f"{name}", "confirm": "aye"},
            cooldown=self.cooldown
        )

        print(response)

        time.sleep(self.cooldown)
        self.status_update()
        return response

    def pray(self):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/pray/",
            headers=header,
            cooldown=self.cooldown
        )

        print(response)

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        self.status_update()
        return response

    def flight(self, direction):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/fly/",
            headers=header,
            data={"direction": f"{direction}"},
            cooldown=self.cooldown
        )

        # print(response)

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        self.cooldown = response["cooldown"]

        time.sleep(self.cooldown)
        return response

    def dash(self, direction, num_rooms, room_ids):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/dash/",
            headers=header,
            data={"direction": f"{direction}",
                  "num_rooms": f"{num_rooms}", "next_room_ids": f"{room_ids}"},
            cooldown=self.cooldown
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        self.cooldown = response["cooldown"]

        time.sleep(self.cooldown)
        return response

    def carry(self, treasure):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/carry/",
            headers=header,
            data={"name": f"{treasure}"},
            cooldown=self.cooldown
        )

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        self.status_update()
        return response

    def receive(self):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/receive/",
            headers=header,
            cooldown=self.cooldown
        )

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        self.status_update()
        return response

    def warp(self):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/warp/",
            headers=header,
            cooldown=self.cooldown
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        # self.cooldown = response["cooldown"]

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        return response

    def recall(self):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/recall/",
            headers=header,
            cooldown=self.cooldown
        )

        self.current_room = response["room_id"]
        self.room_items = response["items"]
        self.room_exits = response["exits"]
        self.errors = response["errors"]
        self.messages = response["messages"]
        # self.cooldown = response["cooldown"]

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        return response

    def wear_item(self, item):
        header = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json",
        }

        response = dreamy.post(
            f"{URL}/api/adv/wear/",
            headers=header,
            data={"name": f"{item}"},
            cooldown=self.cooldown
        )

        self.cooldown = response["cooldown"]
        time.sleep(self.cooldown)
        self.status_update()
        return response
