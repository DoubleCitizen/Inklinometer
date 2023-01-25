class ReaderTxt:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as file:
            text = file.readlines()
        return text