import json
import requests

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def bfs(self, starting_vertex, destination_vertex, player_location):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        # stack a list to use as our path
        q.enqueue([starting_vertex])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1] # Vertex is last item in the stack
            if v not in visited:
                if v == destination_vertex:
                    return path # the path to that destination vertex
                visited.add(v)

                ###This part should be the directions??
                for direction in player_location[v]["exits"].key():
                    new_direction = player_location[v]["exits"][direction]
                    new_path = list(path)
                    if direction == "?":
                        pass
                    else:
                        new_path.append(new_direction)
                        q.enqueue(new_path)
                else:
                    break

def movement(direction, API_KEY):
    movement_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
        headers=movement_header,
        data=json.dumps({"direction": direction}),
    )
    return response

def wise_explorer(direction, API_KEY, room_id):
    movement_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
        headers=movement_header,
        data=json.dumps({"direction": direction, "next_room_id": str(room_id)}),
    )
    return response

def take_treasure(treasure, API_KEY):
    treasure_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/",
        headers=treasure_header,
        data=json.dumps({"name": f"{treasure}"}),
    )
    return response

def drop_treasure(treasure, API_KEY):
    treasure_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/",
        headers=treasure_header,
        data=json.dumps({"name": f"{treasure}"}),
    )
    return response

def sell_treasure(treasure, API_KEY):
    treasure_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/",
        headers=treasure_header,
        data=json.dumps({"name": f"{treasure}", "confirm": "yes"}),
    )
    return response

def status_inventory(API_KEY):
    inventory_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/",
        headers=inventory_header,
        data=json.dumps(),
    )
    return response

def examine(treasure, player, API_KEY):
    inventory_header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/",
        headers=inventory_header,
        data=json.dumps({"name":f"{treasure or player}"}),
    )
    return response

def name_changer(name, API_KEY):
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/",
        headers=header,
        data=json.dumps({"name":f"{name}"}),
    )
    return response

def pray(API_KEY):
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/",
        headers=header,
        data=json.dumps(),
    )
    return response

def flight(direction, API_KEY):
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/",
        headers=header,
        data=json.dumps({"direction":f"{direction}"}),
    )
    return response

def dash(direction, num_rooms, room_id, API_KEY):
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/dash/",
        headers=header,
        data=json.dumps({"direction":f"{direction}", "num_rooms": f"{num_rooms}", "next_room_ids":f"{room_id}"}),
    )
    return response

def carry(treasure, API_KEY)
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/carry/",
        headers=header,
        data=json.dumps({"name":f"{treasure}"}),
    )
    return response
    
def receive( API_KEY)
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/receive/",
        headers=header,
        data=json.dumps(),
    )
    return response

def warp(API_KEY)
    header = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/warp/",
        headers=header,
        data=json.dumps(),
    )
    return response