import json
from collections import defaultdict
from datetime import datetime, timedelta


def merge_twoDict(a, b):  # define the merge_twoDict() function
    return (a.update(b))


class DataInklinometers:
    def __init__(self, path_data1, path_data2, path):
        self.path_data1 = path_data1
        self.path_data2 = path_data2
        self.path = path

    def save_json(self):
        with open(self.path_data1, 'r') as file:
            try:
                data1_list = json.loads(file.read())
            except:
                data1_list = []

        with open(self.path_data2, 'r') as file:
            try:
                data2_list = json.loads(file.read())
            except:
                data2_list = []

        # result_list = []
        # for d in data1_list:
        #     result_list.append(d)
        #
        # for d in data2_list:
        #     merge_twoDict(d, result_list)

        # for dict in data1_list:
        #     dict.value()

        # result_list = {d['key']: d for i in (data1_list, data2_list) for d in i}

        # result_list = []
        # for i, dict in enumerate(data1_list):
        #     print(dict.keys())
        #     print(dict.values())
        #     if dict.keys() == data2_list[i].keys():
        #         result_list.append(merge_twoDict(dict.values(), data2_list[i].values()))
        # print(result_list)

        # print(*data2_list)
        # merge_twoDict(data1_list, **data2_list)
        # print(data1_list)
        new_dict = {}
        result_list = []
        # for dict1 in data1_list:
        #     for dict2 in data2_list:
        #         # print(*dict1)
        #         if str(list(dict1.keys())[0]) == str(list(dict2.keys())[0]):
        #             try:
        #                 used_keys[str(list(dict1.keys())[0])]
        #             except:
        #                 continue
        #             used_keys.append(list(dict1.keys())[0])
        #             dict_1 = dict1[str(list(dict1.keys())[0])]
        #             dict_2 = dict2[str(list(dict2.keys())[0])]
        #             merge_twoDict(dict_1, dict_2)
        #             new_dict[str(list(dict1.keys())[0])] = dict_1
        #             result_list.append(new_dict)

        for i, dict1 in enumerate(data1_list):
            try:
                key_1 = str(list(dict1.keys())[0])
                print(dict1)
                print(key_1)
                # print(key_1)
                dict2 = {key_1: data2_list[i][key_1]}
                dict_1 = dict1[key_1]
                dict_2 = dict2[key_1]
                merge_twoDict(dict_1, dict_2)
                new_dict[key_1] = dict_1
                result_list.append(new_dict)
            except:
                continue
                # print(f"{new_dict}")
        # print(result_list)

        # data[datetime_now_inklinometer] = {**data[datetime_now_inklinometer], "CB": inklinometer.center_bubble}

        # result_list = [dict(i, **j) for i, j in zip(data1_list, data2_list)]
        # print(result_list)

        with open(self.path, "w+") as file:
            file.write(json.dumps(result_list))
