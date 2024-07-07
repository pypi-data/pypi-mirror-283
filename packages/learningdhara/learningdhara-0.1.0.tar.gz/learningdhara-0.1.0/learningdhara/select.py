"""
Customer module to get the customer details

Return customer dictionary
"""

import json


def select_all(file_path, entity="test"):
    """
    Read the json data from data/xxx.json

    Return the json data
    """

    # Check the entity and read
    if entity and file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)

    return data if data else None
