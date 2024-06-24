"""
Puzzle description: https://adventofcode.com/2023/day/8
"""
from pathlib import Path
import sys
import ultraimport
from enum import Enum
import datetime as dt

# from ..utils import utils
# Workaround because I can not get relative imports to work
sys.path.append(str(Path(__file__).parent.parent))

from utils import utils
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")
EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), "example.txt")
EXAMPLE2_PATH = os.path.join(os.path.dirname(__file__), "example2.txt")

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    

def create_next_closure(circular_array:list[str]) -> Direction:
    """
    Implements a closure to get the next direction from the instruction array.
    If we're at the end of the array, we start over at index 0
    
    Args:
        circular_array (list[str]): [the list of L/R instructions]

    Returns:
        next: this is a function that will return the direction to go when called
    """
    
    array_idx = 0
    def inner_next():
        nonlocal array_idx  # Declare array_idx as nonlocal to modify in the closure
        value = circular_array[array_idx]
        if array_idx == len(circular_array) - 1:
            array_idx = 0
        else:
            array_idx += 1
        if value == "L":
            return Direction.LEFT
        return Direction.RIGHT
    return inner_next


def parse_input(input_path:str) -> tuple[list[str], dict[str, list[str]]]:
    """
    Parse the input file and return the data in a usable format.
    
    Returns
        - instructions array: List of L/R instructions
        - node_dict: dict with key node and value it's left and right neighbors
    """
    lines = utils.read_table_from_file(input_path)
    instructions_array = [ch for ch in lines[0].strip()]
    
    node_data = lines[2:]
    node_dict = {}
    for node_repr in node_data:
        node, directions = node_repr.split("=")
        node_val = node.strip()
        left, right = directions.split(",")
        left_node = left.strip("( ")
        right_node = right.strip(") ")
        node_dict[node_val] = [left_node, right_node]
        if node_val == "MTP":
            print(f"MTP! Neighbors: { node_dict[node_val]}")
        
    return instructions_array, node_dict
        
       
def get_num_steps(instructions:list[str], node_to_neighbors:dict[str,list[str]])-> int:
    """
    Args:
        instructions ([str]): List of directions needed to take to get to the final node
        node_to_neighbors ([dict[str], list[str]]): Dict mapping a node to its neigbors

    Returns:
        num_steps[int]: Number of steps taken to reach the end node
    """
    next = create_next_closure(instructions)
    
    # start node is AAA
    curr_node = "AAA"
    # while start node is not ZZZ 
    num_steps = 0
    while curr_node != "ZZZ":
    #   - go the the next node via the L/R instruction
        instruction = next()
        # print(f"node {curr_node} has neighbors {node_to_neighbors[curr_node]}")
        curr_node = node_to_neighbors[curr_node][instruction.value]
        # print(f"instruction: {instruction}")
        # print(f"next_node: {curr_node}")
    #   - increment the steps
        num_steps += 1
    return num_steps

def get_num_steps_part_2(instructions:list[str], node_to_neighbors:dict[str,list[str]])-> int:
    """
    Args:
        instructions ([str]): List of directions needed to take to get to the final node
        node_to_neighbors ([dict[str], list[str]]): Dict mapping a node to its neigbors

    Returns:
        num_steps[int]: Number of steps taken to reach the end node
    """
    # identify all of the starting nodes and make an array
    curr_nodes = []
    # reached_end_state = False 
    # array_idx = 0
    # num_steps = 0
    next = create_next_closure(instructions)
    for node in node_to_neighbors:
        if node[-1] == "A":
            curr_nodes.append(node)
            
    # t = dt.datetime.now()
    curr_node, first_node = curr_nodes[0], curr_nodes[0]
    idx = 0
    num_steps = 0
    num_end_nodes = 0
    while True:
        if instructions[idx] == "L":
            direction = 0
        else:
            direction = 1
        curr_node = node_to_neighbors[curr_node][direction]
        num_steps += 1
        
        if curr_node == first_node and idx == 0:
            break
        if idx == len(instructions) - 1:
            idx = 0
        else:
            idx += 1
        if curr_node[-1] == "Z":
            num_end_nodes += 1
       
    print(num_steps)
    print(f"Number of end nodes encountered: {num_end_nodes}")
    

    

def main():
    # parse the input into a dict of node to L/R instructions and a circular array with direction
    instructions, node_to_neighbors = parse_input(INPUT_PATH)
    # print(f"Instructions: {instructions}")
    # print(f"Node dict: {node_to_neighbors}")
    
    # PART 1
    print(get_num_steps(instructions=instructions, node_to_neighbors=node_to_neighbors))
    
    instructions2, node_to_neighbors2 = parse_input(EXAMPLE2_PATH)
    
    # PART 2
    print(get_num_steps_part_2(instructions, node_to_neighbors))
   
    

if __name__ == "__main__":
    main()