
class ConverterTxtToDict:
    def __init__(self):
        self.list_dicts = []
        self.raw_data_list: list = []
        self.data_list: list = []

    def convert(self, data):
        old_line_list = 0
        i = 0
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            if line_list[2] == 'IRP_MJ_READ' and line_list[4] == 'STATUS_SUCCESS':
                if old_line_list == line_list[1]:
                    i += 1
                    date_time = str(f"{line_list[1]},{i}")
                else:
                    i = 1
                    date_time = str(f"{line_list[1]},{i}")
                coords: str = line_list[6]
                old_line_list = line_list[1]
                try:
                    x_var = float(coords[coords.find('X') + 2:coords.find('Y') - 1])
                    y_var = float(coords[coords.find('Y') + 2:coords.find('T') - 1])
                    t_var = float(coords[coords.find('T') + 2:coords.find('T') + 7])
                    self.raw_data_list.append([date_time, x_var, y_var, t_var])
                except:
                    continue
        for id, val in enumerate(self.raw_data_list):
                date_time = val[0]
                self.data_list.append([date_time, val[1], val[2], val[3]])
        result_dict = {}
        for id, val in enumerate(self.data_list):
            result_dict[val[0].replace("/", "-")] = {"X": val[1], "Y": val[2], "T": val[3]}
        return result_dict



