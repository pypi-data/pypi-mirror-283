"""
New entity addition module
"""
import json
from learningdhara.select import select_all


def insert_me(file_path, entity, **data):
    """
    adding new customer
    """

    if entity and file_path:
        # Load the original data
        load_data = select_all(file_path, entity)
        # Add the new customer to original data
        for item in data["data"]:
            load_data["data"].append(item)

        with open(file_path, "w") as outfile:
            json.dump(load_data, outfile)

    else:
        raise Exception(f"No entity {entity} found in {file_path}.")
