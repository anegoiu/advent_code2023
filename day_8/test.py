"""
File testing the helper functions for the day 8 challenge
"""

from day_8 import (
    EXAMPLE_PATH,
    parse_input
)


def test_parse_input_on_example_data():
    """
    Test the parse_input function on the example data
    """
    expected_instructions_array = "RL"
    expected_nodes = ["AAA", "BBB", "CCC", "DDD", "EEE", "GGG" "ZZZ"]
    instructions, node_to_neighbors = parse_input("example_input.txt")
    assert instructions == expected_instructions_array
    for node in node_to_neighbors:
        assert node in expected_nodes
    assert node_to_neighbors["AAA"] == ["BBB", "CCC"]
    assert node_to_neighbors["BBB"] == ["DDD", "EEE"]


