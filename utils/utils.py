import os
from logging import log

import requests

def main():
    print("Hello, World!")
    curr_dir = (os.getcwd())
    print(f"Current directory: {curr_dir}")
    table_path = os.path.join(curr_dir, "day_7", "cards.txt")
    get_table(table_path, print_table=True)
    


print(f"First module's name: {__name__}")

def scrape_table(day:int, write_path:str=None):
    """
    Function to scrape the table from the advent of code website
    """
    INPUT_URL = f"https://adventofcode.com/2023/day/{day}/input"
    session_cookie = "53616c7465645f5f1126198fd3f94b07080e35bd407e7633af9c0e4acf79ffd0ee60b7e1bb727d72b588adcff2c5ecb9cd9bc494ff04875599471da258136bba"
    input = requests.get(INPUT_URL, cookies={"session": session_cookie})
    if write_path:
        with open(write_path, "w") as f:
            f.write(input.text) 
        # TODO: Add logging
        print("Scraping input for day %s. Input written successfully to %s", day, write_path)
    
    # return input.text
    

def read_table_from_file(path:str, print_table:bool=False):
    """
    Function to read a table from a file
    Inputs:
    - path: path to the file
    - print_table: whether to print the table or not
    """
    text  = open(path).readlines()
    if print_table:
        print(text)
    return [line.strip() for line in text]

def connect_to_advent_code():
    HOME_URL = "https://adventofcode.com/2023/about"
    home_page = requests.get(HOME_URL)
    print(home_page.text)
    """
    Function to connect to the advent of code website
    """
    pass

if __name__ == "__main__":
    print("Script is being executed directly")
    main()