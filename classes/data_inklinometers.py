import json
from json import JSONDecodeError


class DataInklinometers:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def save_json(self):
        with open(self.path, "w") as file:
            file.write(json.dumps(self.data))
