"""
A file solving the mirage maintenance problem of the advent of code:
https://adventofcode.com/2023/day/10
"""
    
from enum import Enum
from pathlib import Path
import sys
from typing import Optional
# Workaround because I can not get relative imports to work
sys.path.append(str(Path(__file__).parent.parent))

import os
from utils import utils
INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt") 
EXAMPLE_PATH =  os.path.join(os.path.dirname(__file__), "example.txt") 

STARTING_CHAR = "S"

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    
    def __eq__(self, other:"Direction"):
        if not isinstance(other, Direction):
            return False
        return self.value == other.value
    
    
PIPE_MAP = utils.read_table_from_file(INPUT_PATH)
EXAMPLE_MAP = utils.read_table_from_file(EXAMPLE_PATH)
USED_MAP = PIPE_MAP
PIPE_MAPPING = {
    "|" : [Direction.UP, Direction.DOWN],
    "-" : [Direction.LEFT, Direction.RIGHT],
    "L" : [Direction.UP, Direction.RIGHT],
    "J" : [Direction.UP, Direction.LEFT],
    "7" : [Direction.DOWN, Direction.LEFT],
    "F" : [Direction.DOWN, Direction.RIGHT], 
}

def get_starting_point() -> tuple[int,int]:
    """
    Returns the starting point of the creature
    """
    for row_idx in range(len(USED_MAP)):
        for col_idx in range(len(USED_MAP[0])):
            if USED_MAP[row_idx][col_idx] == "S":
                return row_idx, col_idx
    
class Connection:
    # define the map we use for the connection class
    pipe_map = USED_MAP
    def __init__(self, x:int, y:int, prev_connection:Direction):
        self.x = x
        self.y = y
        # direction in which this pipe connects to the previous pipe. If this pipe does not have an
        # opening in prev_connection direction, then this conneciton is invalid
        self.prev_connection = prev_connection
        # ensure x and y are not out of bounds before assigning pipe character
        if (
        self.x >= 0 and
        self.x < len(self.pipe_map) and 
        self.y >= 0 and
        self.y < len(self.pipe_map[0])
        ):
            self.char = self.pipe_map[x][y]
        else:
            self.char = None
        
    def get_next_connection(self) -> Optional["Connection"]:
        """
        Guarantees: This method should only be called if the current connection is valid
       
        Return the other direction this pipe connects to. It will determine the 
        cycle path.
        Returns None if connection is invalid"""
        if not self.is_valid():
            raise TypeError("Tried to get new connection for invalid current connection")
        # get the direction this pipe must connect to the next pipe
        pipe_direction = [direction for direction in PIPE_MAPPING[self.char] if direction != self.prev_connection]
        assert len(pipe_direction) == 1
        # we want to give the complement of the connection. this pipe connects to the right but it
        # will conenct from the left of the new connection
        if pipe_direction[0] == Direction.LEFT:
            return Connection(self.x, self.y-1, Direction.RIGHT)
        if pipe_direction[0] == Direction.RIGHT:
            return Connection(self.x, self.y+1, Direction.LEFT)
        if pipe_direction[0] == Direction.UP:
            return Connection(self.x-1, self.y, Direction.DOWN)
        if pipe_direction[0] == Direction.DOWN:
            return Connection(self.x+1, self.y, Direction.UP)
    
    def __str__(self):
        return f"Postition ({self.x}, {self.y})| Pipe: {self.char}, prev_con: {self.prev_connection}" 
    
    
    def is_valid(self) -> bool:
        """
        Returns True if this Conenction is a pipe that is connected to the previous
        connection
        """
        
        if self.x < 0 or self.x >= len(self.pipe_map) or self.y < 0 or self.y >= len(self.pipe_map[0]):
            return False
        if self.char == ".":
            return False
        if self.prev_connection not in PIPE_MAPPING[self.char]:
            return False
        return True


def find_steps_in_loop():
    """
    Finds the number of steps from the farthest away pipe in the loop
    Args:
        pipe_map: map of pipes
        x, y: position of the starting pipe
    Returns:
       num_steps: int 
    """
    x, y = get_starting_point()
     # assume the starting point is a 4 way intersaection. 
    connections = []
    # we go down =>  prev_connection is up
    connections.append(Connection(x+1, y, Direction.UP))
    # we go up => prev_connection is down
    connections.append(Connection(x-1, y,Direction.DOWN))
    # we go left
    connections.append(Connection(x, y-1, Direction.RIGHT))
    connections.append(Connection(x, y+1, Direction.LEFT))
    # start tracversing lopps in all directions one step at time
    num_steps = 1
    while True:
        print("------------------")
        print(f"step {num_steps}")
        for connection in connections:
            print(connection)
        assert len(connections) >= 2
        num_steps += 1
        
        new_connections = []
        positions = {(connection.x, connection.y) for connection in connections}
        for connection in connections:
            # only add connection if it's valid
            if connection.is_valid():
                new_connection =  connection.get_next_connection()
                print("connection", connection)
                print(f"new conenctions: {new_connection}")
                # found the loop, return # steps
                if (new_connection.x, new_connection.y) in positions:
                    # we need to add one because we would have only reached this point on the next
                    # step
                    return num_steps
                positions.add((new_connection.x, new_connection.y))
                new_connections.append(new_connection)
        #  continue the procces swith next iteraton of connectinos 
        connections = new_connections

def main():
    num_steps = find_steps_in_loop()
    print("Number of steps", num_steps)
   
                    
  
         
    # keep a list of curr position, and next direction on every loop
    # if any 2 loop end up on the same spot, we are done
   
if __name__ == "__main__":
    main()
    
