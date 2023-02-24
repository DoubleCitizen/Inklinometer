import collections
from datetime import datetime, timedelta

from classes.data_inklinometers import DataInklinometers
from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.inklinometer import Inklinometer
from utils.config import options_dict
from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
from classes.save_inklinometer_data import SaveInlinometerData
import cv2

trackbars = Trackbars("data/data.json")
# camera = Camera("output_video2.avi")
camera = Camera(0)
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

converter_txt_to_dict = ConverterTxtToDict()
while True:

    success, img = camera.get_image()
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, img)
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

        save_inklinometer2 = SaveInlinometerData('data/data_inklinometer_2.json', now_dict_data)
        save_inklinometer2.save_json()
        now_dict_data = {}

    data = converter_txt_to_dict.convert(data=reader_txt.read())
    if data is not None:
        save_inklinometer1 = SaveInlinometerData('data/data_inklinometer_1.json', data)
        save_inklinometer1.save_json()

    # [last_key] = collections.deque(data, maxlen=1)
    # print(f"{last_key} * {datetime_now_inklinometer} {last_key==datetime_now_inklinometer}")
    # data["2023-01-25 15:17:09"] = data[datetime_now_inklinometer] + dict({inklinometer.center_bubble})
    # print(data.update(now_dict_data))
    # print(dict(data, **now_dict_data))
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

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
