import json
from typing import List, Dict, Tuple


class Database:
    def __init__(self, filename="scraped_data.json"):
        """
        Initialize the Database with the given filename.
        """

        self.filename = filename

    def save(self, data: List[Dict], key: str) -> Tuple[int, int]:
        """
        Save the data to a JSON file. If the key exists, update the value; otherwise, insert it.
        Return a tuple with counts of updated and inserted items.
        """

        updated_count = 0
        inserted_count = 0

        if not data:
            return updated_count, inserted_count

        existing_data = self.load()
        existing_data_dict = {item[key]: item for item in existing_data}

        for new_item in data:
            if new_item[key] in existing_data_dict:
                updated_count += 1
            else:
                inserted_count += 1
            existing_data_dict[new_item[key]] = new_item

        updated_data = list(existing_data_dict.values())

        with open(self.filename, "w") as file:
            json.dump(updated_data, file, indent=4)

        return updated_count, inserted_count

    def load(self) -> List[Dict]:
        """
        Load the data from a JSON file.
        """

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []


database = Database()
