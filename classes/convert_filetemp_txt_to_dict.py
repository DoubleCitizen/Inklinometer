from classes.read_file import ReaderTxt


class ConverterTxtToDict:
    def __init__(self):
        self.list_dicts = []
        self.raw_data_list: list = []
        self.data_list: list = []

    def convert(self, data):
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            if line_list[2] == 'IRP_MJ_READ' and line_list[4] == 'STATUS_SUCCESS':
                try:
                    date_time = line_list[1]
                    temperature = float(line_list[6])
                    self.raw_data_list.append([date_time, temperature])
                except:
                    pass

        summ = [0]
        counter = 1
        for id, val in enumerate(self.raw_data_list):
            if len(self.raw_data_list) - 1 > id:
                val_next = self.raw_data_list[id + 1]
            if val_next[0] == val[0]:
                counter += 1
                summ = [summ[0] + val_next[1]]
            else:
                date_time = val[0]
                self.data_list.append([date_time, summ[0] / counter])
                counter = 1
                summ = [val[1]]
        result_dict = {}
        for id, val in enumerate(self.data_list):
            result_dict[val[0].replace("/", "-")] = {"T": val[1]}
        return result_dict