from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")


class Player:
    def __init__(self, starting_room, name = "User"):
        self.name = name,
        self.self.API_KEY,
        self.current_room = starting_room,
        self.cooldown = 1,
        self.encumbrance = 2,
        self.strength = 0,
        self.speed = 0,
        self.gold = 0,
        self.bodywear = None,
        self.footwear = None,
        self.inventory = [],
        self.status = [],
        self.errors = [],
        self.messages = [],

    def add_to_inventory(self, item):
        self.inventory.append(item)




    def movement(self, direction):
        movement_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}/api/adv/move/",
                    headers=movement_header,
                    data=json.dumps({"direction": direction}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def wise_explorer(self, direction, room_id):
        movement_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/move/",
                    headers=movement_header,
                    data=json.dumps({"direction": direction, "next_room_id": str(room_id)})
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def take_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/take/",
                    headers=treasure_header,
                    data=json.dumps({"name": f"{treasure}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def drop_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/drop/",
                    headers=treasure_header,
                    data=json.dumps({"name": f"{treasure}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def sell_treasure(self, treasure):
        treasure_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/sell/",
                    headers=treasure_header,
                    data=json.dumps({"name": f"{treasure}", "confirm": "yes"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def status_inventory(self):
        inventory_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/status/",
                    headers=inventory_header,
                    data=json.dumps(),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def examine(self, treasure, player):
        inventory_header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/examine/",
                    headers=inventory_header,
                    data=json.dumps({"name":f"{treasure or player}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def name_changer(self, name):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/change_name/",
                    headers=header,
                    data=json.dumps({"name":f"{name}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def pray(self):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/pray/",
                    headers=header,
                    data=json.dumps(),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def flight(self, direction):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{TEST_URL}api/adv/fly/",
            headers=header,
            data=json.dumps({"direction":f"{direction}"}),
        )

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/fly/",
                    headers=header,
                    data=json.dumps({"direction":f"{direction}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def dash(self, direction, num_rooms, room_id):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/dash/",
                    headers=header,
                    data=json.dumps({"direction":f"{direction}", "num_rooms": f"{num_rooms}", "next_room_ids":f"{room_id}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def carry(self, treasure):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/carry/",
                    headers=header,
                    data=json.dumps({"name":f"{treasure}"}),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response
        
    def receive(self):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/receive/",
                    headers=header,
                    data=json.dumps(),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response

    def warp(self):
        header = {
            "Authorization": f"Token {self.API_KEY}",
            "Content-Type": "application/json",
        }

        successful = False
        while not successful:
            try:
                response = requests.post(
                    f"{TEST_URL}api/adv/warp/",
                    headers=header,
                    data=json.dumps(),
                ).json()
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)
                time.sleep(self.cooldown)
                
        return response