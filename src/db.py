import json
from typing import List, Dict


class Database:
    def __init__(self, filename="scraped_data.json"):
        """
        Initialize the Database with the given filename.
        """

        self.filename = filename

    def save(self, data: List[Dict]):
        """
        Save the data to a JSON file.
        """

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

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