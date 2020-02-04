import json
import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")



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
        ##Change bfs to take treasure, and then revert to shop at 9 treasure?
        #Check status at each treasure pick up
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

