import json


class JSONModule:
    def __init__(self, path):
        self._path = path

    def get(self, var_name):
        with open(self._path, 'r') as file:
            try:
                data = json.loads(file.read())
            except:
                data = {}
        result = data.get(var_name, "")
        return result

    def set(self, var_name, value):
        with open(self._path, 'r') as file:
            try:
                data = json.loads(file.read())
            except:
                data = {}

        data[var_name] = value

        with open(self._path, "w+") as file:
            file.write(json.dumps(data))
