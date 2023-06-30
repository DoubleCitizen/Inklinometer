
class ConverterTxtToDict:
    def __init__(self):
        self.list_dicts = []
        self.raw_data_list: list = []
        self.data_list: list = []

    def convert(self, data):
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            if line_list[2] == 'IRP_MJ_READ' and line_list[4] == 'STATUS_SUCCESS':
                date_time = line_list[1]
                coords: str = line_list[6]
                x_var = float(coords[coords.find('X') + 2:coords.find('Y') - 1])
                y_var = float(coords[coords.find('Y') + 2:coords.find('T') - 1])
                t_var = float(coords[coords.find('T') + 2:coords.find('T') + 7])
                self.raw_data_list.append([date_time, x_var, y_var, t_var])
        summ = [0, 0, 0]
        counter = 1
        for id, val in enumerate(self.raw_data_list):
            if len(self.raw_data_list) - 1 > id:
                val_next = self.raw_data_list[id + 1]
            if val_next[0] == val[0]:
                counter += 1
                summ = [summ[0] + val_next[1], summ[1] + val_next[2], summ[2] + val_next[3]]
            else:
                date_time = val[0]
                self.data_list.append([date_time, summ[0] / counter, summ[1] / counter, summ[2] / counter])
                counter = 1
                summ = [val[1], val[2], val[3]]
        result_dict = {}
        for id, val in enumerate(self.data_list):
            result_dict[val[0].replace("/", "-")] = {"X": val[1], "Y": val[2], "T": val[3]}
        return result_dict



