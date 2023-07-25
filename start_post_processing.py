from datetime import datetime, timedelta

import numpy as np

from classes.data_inklinometers import DataInklinometers
from classes.json_module import JSONModule
from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.inklinometer import Inklinometer
from utils.config import options_dict
from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
from classes.save_inklinometer_data import SaveInlinometerData
from classes.timer import Timer
import cv2

file_name = 'inklin_2023_07_15_18_46_34.mp4'

trackbars = Trackbars("data/data.json")
# camera = Camera("output_video2.avi")
camera = Camera(f'data/{file_name}')
name_of_window = "Test"
inklinometer = Inklinometer(camera=camera, trackbars=trackbars, options=options_dict)
json_module = JSONModule('data/variables.json')


def get_time_from_inklin_file(file_name: str):
    file_name = file_name[file_name.find('_') + 1:file_name.find('.')]
    date_time_obj = datetime.strptime(file_name, '%Y_%m_%d_%H_%M_%S')
    return date_time_obj


now_dict_data = {}
new_dict = {}
date_time_str_list = []
CB_sum = 0
CB_n = 0
CB_aver = 0
start_time = get_time_from_inklin_file(file_name)

converter_txt_to_dict = ConverterTxtToDict()

t = Timer()
t.start()
seconds_passed_real = 0
seconds_left_real = 0

old_seconds_passed = 0
seconds_passed = 0
i = 0
count = 0
while True:
    count += 1

    seconds_passed = int(camera.get_frames() / camera.get_fps())
    if seconds_passed == old_seconds_passed:
        i += 1
    else:
        i = 1
    old_seconds_passed = seconds_passed

    seconds_left = int(abs(camera.get_all_frames() // camera.get_fps()) - int(seconds_passed))
    if int(seconds_passed) != 0:
        seconds_left_real = int((t.get_time() / int(seconds_passed)) * seconds_left)
        seconds_passed_real = int((t.get_time() / int(seconds_passed)) * int(seconds_passed))

    seconds_passed_str = str(seconds_passed)
    milliseconds = int(seconds_passed_str[seconds_passed_str.find('.') + 1:seconds_passed_str.find('.') + 4])

    datetime_now_inklinometer = str(f"{start_time + timedelta(seconds=int(seconds_passed))},{i}")

    date_time_str_list.append(datetime_now_inklinometer)

    now_dict_data[date_time_str_list[-1]] = {"CB": inklinometer.center_bubble}

    save_inklinometer2 = SaveInlinometerData('data/data_inklinometer_pp.json', now_dict_data)
    save_inklinometer2.save_json()

    inklinometer.main()
    trackbars.save()

    winfo = np.zeros((512, 512, 3), np.uint8)
    if CB_n != 0:
        CB_aver = CB_sum / CB_n
    linregress_CV_VIM_slope = json_module.get('linregress_CV_VIM_slope')
    linregress_CV_VIM_intercept = json_module.get('linregress_CV_VIM_intercept')

    CB_aver = CB_aver * linregress_CV_VIM_slope + linregress_CV_VIM_intercept
    CB_aver = round(CB_aver, 3)
    winfo2 = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(winfo2, f"Видеоинклинометр = {round((CB_aver / 0.0047), 3)}''", (0, 120), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2, f"Видеоинклинометр = {CB_aver}mrad", (0, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)

    cv2.putText(winfo2,
                f"Прошло времени = {seconds_passed_real // 60 // 60}:{(seconds_passed_real // 60) % 60}:{seconds_passed_real % 60}",
                (0, 180), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2,
                f"(кадровые) = {int(seconds_passed) // 60 // 60}:{(int(seconds_passed) // 60) % 60}:{int(seconds_passed) % 60}",
                (0, 210), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2,
                f"Осталось времени = {seconds_left_real // 60 // 60}:{(seconds_left_real // 60) % 60}:{seconds_left_real % 60}",
                (0, 240), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)
    cv2.putText(winfo2,
                f"(кадровые) = {seconds_left // 60 // 60}:{(seconds_left // 60) % 60}:{seconds_left % 60}",
                (0, 270), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                (0, 150, 0),
                2)

    cv2.imshow("Window", winfo2)

    if (cv2.waitKey(1) & 0xFF == ord('q')) or (seconds_left <= 0 and seconds_passed >= 1):
        print("count", count)
        print("camera_all_frames", camera.get_all_frames())
        print(len(date_time_str_list))
        break
