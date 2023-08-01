class ConverterTxtToDict:
    def __init__(self):
        self.result_dict = {}

    def convert(self, data):
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            datetime = line_list[0]
            center_bubble = line_list[1][:line_list[1].find('\n')]
            self.result_dict[datetime] = {'CB': center_bubble}
        return self.result_dict


