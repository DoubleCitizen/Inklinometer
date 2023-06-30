import json


def merge_twoDict(a, b):  # define the merge_twoDict() function
    return (a.update(b))


class SaveInlinometerData:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def save_json(self):
        try:
            with open(self.path, 'r') as file:
                try:
                    data = json.loads(file.read())
                except:
                    data = {}

            merge_twoDict(data, self.data)
        except:
            data = self.data

        with open(self.path, "w+") as file:
            file.write(json.dumps(data))
