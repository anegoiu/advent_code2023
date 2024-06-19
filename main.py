"""
Main script to run the code for the day.
The scripts expects that we run it from the main directory

Arguments:
- day: the day of the advent of code

Example Usage:
```bash
python main.py --day 7
```
"""
import argparse
 
parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


from utils import utils
from day_7 import camel_cards
import os

TABLE_PATH = os.path.join(os.getcwd(), "day_7", "cards.txt")

# TODO: Add parser and add a day argument 
# Also add a scrape_input one to say wether we want to scrape the data or not (limit webscraping)
def main():
    """
    Main function to run the script.
    """
    # TODO: Remove once script takes on arguments
    # Set the arguments
    day = 7
    
    input_path = os.path.join(os.getcwd(), f"day_{day}", "input.txt")
    
    # limit web scraping: only scrape if we are missing the input text 
    if not os.path.exists(input_path):
        utils.scrape_table("7", write_path=input_path)
    
    # Run the code for the day
    camel_cards.main()
    

if __name__ == "__main__":
    main()