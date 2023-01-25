from datetime import datetime


class ConverterTxtToDict:
    def __init__(self, data):
        self.data = data

    def convert(self):
        data_dict = {}
        for id, val in enumerate(self.data):
            find_read_data = val.find("Read data")
            find_x = val.find("X:")
            find_y = val.find("Y:")
            if find_read_data != -1:
                date_time_str = val[1:20]
                date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')
                date_time_str = str(date_time_obj)
            if find_x != -1:
                X = val[find_x:find_x + 8]
                data_list = []
                data_list.append(X)
            if find_y != -1:
                Y = val[find_y:find_y + 8]
                T = val[find_y + 9:find_y + 16]
                data_list.append(Y)
                data_list.append(T)
                data_dict[date_time_str] = {data_list[0][0]: float(data_list[0][2:len(data_list[0])]),
                    data_list[1][0]: float(data_list[1][2:len(data_list[0])]),
                    data_list[2][0]: float(data_list[2][2:len(data_list[0])]),}
                data_list = []
        return data_dict
