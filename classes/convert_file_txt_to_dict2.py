from datetime import datetime, timedelta


class ConverterTxtToDict:
    def __init__(self):
        self.date_time_str_list = []
        self.list_dicts = []
        self.data_dict = {}
        self.data_list = []
        self.date_time_str = ""

    def convert(self, data):
        for id, val in enumerate(data):
            datetime_now_inklinometer = str(datetime.now().replace(microsecond=0) - timedelta(seconds=0))
            find_x = val.find("X:")
            find_y = val.find("Y:")
            find_t = val.find("T:")

            date_time_str = datetime_now_inklinometer
            self.date_time_str = str(date_time_str)

            if find_x != -1:
                X = val[find_x:find_x + 8]
                self.data_list = []
                self.data_list.append(X)
            if find_y != -1:
                Y = val[find_y:find_y + 8]
                T = val[find_t:find_t + 7]
                self.data_list.append(Y)
                self.data_list.append(T)
                x_key = self.data_list[0][0]
                y_key = self.data_list[1][0]
                t_key = self.data_list[2][0]
                x_val = float(self.data_list[0][2:len(self.data_list[0])])
                y_val = float(self.data_list[1][2:len(self.data_list[0])])
                t_val = float(self.data_list[2][2:len(self.data_list[0])])
                self.data_dict[self.date_time_str] = {x_key: x_val,
                                                      y_key: y_val,
                                                      t_key: t_val, }
                self.date_time_str_list.append(self.date_time_str)
                if len(self.list_dicts) < 1:
                    self.list_dicts.append(self.data_dict)
                    # print(self.list_dicts[-1])

                for key, val in self.list_dicts[-1].items():
                    if key == self.date_time_str_list[0]:
                        # print(f"key = {key}; self.date_time_str_prev = {self.date_time_str_list[0]}")
                        # print(f"{key==self.date_time_str_list[0]}")
                        self.list_dicts.append(self.data_dict)
                        # print(f"i = {self.i}")
                    else:
                        x_sum = 0
                        y_sum = 0
                        t_sum = 0
                        n = 0
                        now_time = self.date_time_str_list[0]
                        # print(self.list_dicts)
                        for id, dict in enumerate(self.list_dicts):
                            try:
                                x_sum += dict[now_time]['X']
                                y_sum += dict[now_time]['Y']
                                t_sum += dict[now_time]['T']
                                n = id + 1
                            except KeyError:
                                break
                        x_aver = x_sum / n
                        y_aver = y_sum / n
                        t_aver = t_sum / n
                        result_dict = {self.date_time_str_list[0]: {'X': x_aver, 'Y': y_aver, 'T': t_aver}}
                        self.date_time_str_list = []
                        self.list_dicts = []

                        return result_dict
                    # print(self.list_dicts)

                self.data_dict = {}
                self.data_list = []
