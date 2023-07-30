import collections
from datetime import datetime, timedelta

import numpy as np

from classes.data_inklinometers import DataInklinometers
from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.inklinometer import Inklinometer
from utils.config import options_dict
from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
from classes.json_module import JSONModule
from classes.save_inklinometer_data import SaveInlinometerData
import cv2

trackbars = Trackbars("data/data.json")
# camera = Camera("output_video2.avi")
camera = Camera("data/inklin_2023_07_28_16_11_26.mp4")
# camera = Camera(1)
name_of_window = "Test"
inklinometer = Inklinometer(camera=camera, trackbars=trackbars, options=options_dict)


def merge_twoDict(a, b):  # define the merge_twoDict() function
    return (a.update(b))


now_dict_data = {}
new_dict = {}
reader_txt = ReaderTxt("data/data_port_spy_2.txt")
date_time_str_list = []
CB_sum = 0
CB_n = 0
CB_aver = 0
nivel_deviation = 0
json_module = JSONModule('data/variables.json')
converter_txt_to_dict = ConverterTxtToDict()

while True:

    success, img = camera.get_image()
    # cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    # cv2.imshow(name_of_window, img)
    data_inklinometer = {}

    datetime_now_inklinometer = str(datetime.now().replace(microsecond=0) - timedelta(seconds=0))
    date_time_str_list.append(datetime_now_inklinometer)
    if date_time_str_list[0] == date_time_str_list[-1]:
        CB_n += 1
        CB_sum += inklinometer.center_bubble
    else:
        CB_aver = CB_sum / CB_n
        now_dict_data[date_time_str_list[0]] = {"CB": CB_aver}
        CB_n = 0
        CB_sum = 0
        date_time_str_list = []

        now_dict_data = {}

    data = converter_txt_to_dict.convert(data=reader_txt.read())

    try:
        # data[datetime_now_inklinometer] = {**data[datetime_now_inklinometer], "CB": inklinometer.center_bubble}
        new_dict[str(datetime.now().replace(microsecond=0) - timedelta(seconds=1))] = {
            **data[datetime_now_inklinometer], "CB": CB_aver}
        # print({**data["2023-01-25 15:52:30"], "CB": inklinometer.center_bubble})
    except:
        pass
    # data_inklinometers = DataInklinometers("data/data_inklinometer_1.json", "data/data_inklinometer_2.json",
    #                                        "data/data_inklinometers.json")
    # data_inklinometers.save_json()
    inklinometer.main()
    trackbars.save()

    winfo = np.zeros((512, 512, 3), np.uint8)
    if CB_n != 0:
        CB_aver = CB_sum / CB_n

    linregress_CV_VIM_slope = json_module.get('linregress_CV_VIM_slope')
    linregress_CV_VIM_intercept = json_module.get('linregress_CV_VIM_intercept')

    CB_aver = CB_aver * linregress_CV_VIM_slope + linregress_CV_VIM_intercept
    # dif = nivel_deviation - CB_aver
    # print(CB_aver * linregress_CV_VIM_slope - dif)
    CB_aver = round(CB_aver, 3)
    difference = abs(round((nivel_deviation-CB_aver),3))

    winfo2 = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(winfo2, f"Видеоинклинометр = {round((CB_aver / 0.0047), 3)}''", (0, 120), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2, f"Видеоинклинометр = {CB_aver}mrad", (0, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)

    try:
        if data is not None:
            for d in data.values():
                nivel_deviation = round(d['X'], 3)
    except:
        pass

    json_module.set('vim', CB_aver)
    json_module.set('nivel220', nivel_deviation)

    cv2.putText(winfo2, f"Nivel220 = {nivel_deviation}mrad", (0, 180), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2, f"Difference = {difference}mrad", (0, 210), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2, f"Difference = {abs(round((difference/0.0047), 3))}''", (0, 240),
                cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.imshow("Window", winfo2)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
