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

        new_dict = {}
        result_list = []


        for i, dict1 in enumerate(data1_list):
            try:
                key_1 = str(list(dict1.keys())[0])
                print(dict1)
                print(key_1)
                dict2 = {key_1: data2_list[i][key_1]}
                dict_1 = dict1[key_1]
                dict_2 = dict2[key_1]
                merge_twoDict(dict_1, dict_2)
                new_dict[key_1] = dict_1
                result_list.append(new_dict)
            except:
                continue

        with open(self.path, "w+") as file:
            file.write(json.dumps(result_list))
