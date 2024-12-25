import json
from typing import List, Dict


class Database:
    def __init__(self, filename="scraped_data.json"):
        self.filename = filename

    def save(self, data: List[Dict]):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self) -> List[Dict]:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
