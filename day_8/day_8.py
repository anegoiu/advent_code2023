"""
Puzzle description: https://adventofcode.com/2023/day/8
"""
from collections import defaultdict
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


def find_cycle(starting_node, instructions, node_to_neighbors):
    """
    Given the starting node, the list of directions and the node map this function identifies when 
    we reach a cycle on the path of the starting node.
    
    Returns the cycle length and the offset.

    The cycle length is defined by the number of steps we take in between 2 visits of the endnoe
    The offset is the # steps from the start node to the end node
    
    Assumption: there is only one end node on the path of each start node. (This is true for our
    input data)

    """
    found_cycle = False
    curr_node = starting_node
    idx = 0
    num_steps = 0
    offset, found_the_end_node = None, False
    
    while not found_cycle:
        if instructions[idx] == "L":
            direction = 0
        else:
            direction = 1
        curr_node = node_to_neighbors[curr_node][direction]
        num_steps += 1
        
        #  find next index in the instructions array
        if idx == len(instructions) - 1:
            idx = 0
        else:
            idx += 1
            
        # count step if we're on end node and check if we're in a cycle
        if curr_node[-1] == "Z":
            # if this is the first time we reach this end node, record offset from start
            if curr_node and not found_the_end_node:
                offset = num_steps
                found_the_end_node = True
            else:
                if (num_steps - offset) % len(instructions) == 0:
                    print("We found cycle")
                    return offset, num_steps - offset

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
    for node in node_to_neighbors:
        if node[-1] == "A":
            curr_nodes.append(node) 
   
    # Mapping from start node to its offset from the start & it's cycle length
    start_node_to_cycle: dict[str, dict[str:int]] =defaultdict(dict) # definiytion of inner dict :offset, length
    for starting_node in curr_nodes:
        offset, cycle_length = find_cycle(starting_node, instructions, node_to_neighbors)
        start_node_to_cycle[starting_node]["offset"] = offset
        start_node_to_cycle[starting_node]["length"] = cycle_length
       
    print(f"end nodes encountered: {start_node_to_cycle}")
    
    #  need to solve this system of eq
    # 21883 + 43766x = 19667 + 39334y = 14681 + 29362z = 16897 + 26038w = 11911 + 23822u .. etc
    
    # find least common denominator 
    max_cyc_node, biggest_cycle = None, 0
    for node, cycle in start_node_to_cycle.items():
        if cycle["length"] > biggest_cycle:
            max_cyc_node = node
            biggest_cycle = cycle["length"]
            
    max_cyc_offset = start_node_to_cycle[max_cyc_node]["offset"]
    convergence_step_candidate = max_cyc_offset + biggest_cycle
    # for every step that reaches the end on this node's path,check if the other nodes converge
    while True:
        convergence_step_candidate += biggest_cycle
        has_converged = True
        for cycle in start_node_to_cycle.values():
            has_converged = has_converged and (convergence_step_candidate - cycle["offset"]) % cycle["length"] == 0
        if has_converged:
            return convergence_step_candidate
        
    
    

    

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