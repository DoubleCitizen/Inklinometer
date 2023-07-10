class ReaderTxt:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()
            last_line = lines[-6:-1]
        return last_line

    def read_all(self, encod=None):
        with open(self.path, 'r', encoding=encod) as file:
            lines = file.readlines()
        return lines