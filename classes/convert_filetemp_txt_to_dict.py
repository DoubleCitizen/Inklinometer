from datetime import datetime, timedelta

from classes.read_file import ReaderTxt


class ConverterTxtToDict:
    def __init__(self):
        self.list_dicts = []
        self.raw_data_list: list = []
        self.data_list: list = []

    def convert(self, data):
        temp_list = []
        long_string = ''
        temp_string = ''
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            if line_list[2] == 'IRP_MJ_READ' and line_list[4] == 'STATUS_SUCCESS' and len(line_list[6]) > 2 and \
                    line_list[6].find('.') != 0 and len(line_list[6]) < 7 and len(line_list[6]) > 3:
                if line_list[6].count('00.') != 0 and line_list[6].count('.00.') == 0:
                    continue
                line_list[6] = line_list[6].replace('0..', '0')
                line_list[6] = line_list[6].replace('00.', '0')

                temperature = float(line_list[6])
                date_time_str = line_list[1]
                date_time = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')
                if len(self.raw_data_list) != 0:
                    date_time_str_prev = self.raw_data_list[-1][0]
                    temperature_prev = self.raw_data_list[-1][1]
                    date_time_prev = datetime.strptime(date_time_str_prev, '%d/%m/%Y %H:%M:%S')
                    # print(date_time - date_time_prev)
                    if abs(temperature - temperature_prev) > 8 and date_time - date_time_prev < timedelta(minutes=10):
                        continue
                self.raw_data_list.append([date_time_str, temperature])

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
