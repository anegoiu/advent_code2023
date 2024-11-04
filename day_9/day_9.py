"""
A file solving the mirage maintenance problem of the advent of code:
https://adventofcode.com/2023/day/9
"""
    
from pathlib import Path
import sys
# Workaround because I can not get relative imports to work
sys.path.append(str(Path(__file__).parent.parent))

import os
from utils import utils
INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt") 
    
def parse_input() -> list[list[int]]:
    """
    This function takes the inpout path, parses out the histories in each line of input
    and returns a list of ints for each line
    """
    input_lines = utils.read_table_from_file(INPUT_PATH)
    histories = []
    for line in input_lines:
        # pull integers from a line of input 
        histories.append([int(value) for value in line.strip().split(" ")])
    return histories
        
    
    
def compute_prediction(history:list[int]) -> int:
    """
    Takes in the history of one environmental value and returns the prediction for it's next 
    value

    Args:
        history (list[int]): list of measurements for the environmental value
    """
    
    prev_arr = []
    tracked_index = None
    
    for val in history:
        curr_arr = [val]
        for prev_v in prev_arr:
            # if there is a rtacked index, we chacke that there is a 0 at the tracked index
            # if not => tracked index is None
            
            curr_arr.append(curr_arr[-1] - prev_v)
            
            # If we reached the last val in history and we have a travcked index => we can end early
        prev_arr = curr_arr
        
        # if curr_arr[-1] == 0:
        #     tracked_index = len(curr_arr) - 1
    # print("prev_arr", prev_arr)
    return sum(prev_arr)


def compute_prediction_backwards(history:list[int]) -> int:
    """_summary_

    Args:
        history (list[int]): the list of measurments of an environmental value

    Returns:
        int: the prediction for the start of the sequence
    """
    prediction_lists = [history]
    while True:
        last_list = prediction_lists[-1]
        new_list = []
        end = 1
        while end < len(last_list):
            new_list.append(last_list[end] - last_list[end-1])
            end += 1
        
        prediction_lists.append(new_list)
        # print(new_list)
        if sum(new_list) == 0:
            break    
    beggining_prediction = 0
    idx = len(prediction_lists) - 1
    while idx >= 0:
        beggining_prediction =prediction_lists[idx][0] -  beggining_prediction
        idx -= 1
        # print(beggining_prediction)     
    return beggining_prediction 
        

def main():
    histories = parse_input()
    print(f"first line: {histories[0]}")
    # check the prediction function
    test_input= [1,2,3,4,5]
    assert compute_prediction(test_input) == 6
    test_input2 = [0,0,0,0]
    assert compute_prediction(test_input2) == 0
    test_input3 = [1, 6, 4, 1]
    print("prediction", compute_prediction(test_input3))
    
    test_input4 = [10,13,16,21,30,45]
    assert compute_prediction_backwards(test_input4) == 5
    results:list[int] = []
    back_results: list[int] = [] 
    
    for history in histories:
        results.append(compute_prediction(history))
        back_results.append(compute_prediction_backwards(history))
    # print(f"predictions: {results}")
    print(f"sum of prediticons: {sum(results)}")
    print(f"sum of backwards predictions {sum(back_results)}")
     


if __name__ == "__main__":
    main()
   