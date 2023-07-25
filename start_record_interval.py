import os
from datetime import datetime, timedelta

from classes.camera import Camera
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
import cv2

from classes.read_file import ReaderTxt
from classes.timer import Timer

camera = Camera('output_video2.avi')

converter_txt_to_dict = ConverterTxtToDict()

success, img = camera.get_image()
width, height = img.shape[:2]

path = "data"

datetime_start_inklinometer = str(datetime.now().replace(microsecond=0) - timedelta(seconds=0))
datetime_start_inklinometer = datetime_start_inklinometer.replace('-', '_')
datetime_start_inklinometer = datetime_start_inklinometer.replace(':', '_')
datetime_start_inklinometer = datetime_start_inklinometer.replace(' ', '_')
if not os.path.isdir(f'data/video_pack_{datetime_start_inklinometer}'):
    os.mkdir(f'data/video_pack_{datetime_start_inklinometer}')
output = cv2.VideoWriter(f'{path}/video_pack_{datetime_start_inklinometer}/inklin_{datetime_start_inklinometer}.mp4',
                         cv2.VideoWriter_fourcc(*'mp4v'), 30.0,
                         (height, width))

reader_txt = ReaderTxt("data/data_port_spy_2.txt")

relax_time = timedelta(seconds=5)
record_time = timedelta(seconds=2)
is_relax = False

t = Timer()
t.start()
current_time = timedelta(seconds=0)

while True:

    seconds_passed = timedelta(seconds=int(t.get_time()))

    if relax_time < seconds_passed - current_time and is_relax:
        datetime_now_inklinometer = str(datetime.now().replace(microsecond=0) - timedelta(seconds=0))
        datetime_now_inklinometer = datetime_now_inklinometer.replace('-', '_')
        datetime_now_inklinometer = datetime_now_inklinometer.replace(':', '_')
        datetime_now_inklinometer = datetime_now_inklinometer.replace(' ', '_')
        output = cv2.VideoWriter(
            f'{path}/video_pack_{datetime_start_inklinometer}/inklin_{datetime_now_inklinometer}.mp4',
            cv2.VideoWriter_fourcc(*'mp4v'), 30.0,
            (height, width))
        current_time = seconds_passed
        is_relax = False
    elif record_time < seconds_passed - current_time and not is_relax:
        current_time = seconds_passed
        is_relax = True

    if is_relax:

        cv2.destroyAllWindows()
        output.release()
        camera.cap.release()
    else:
        success, img = camera.get_image()
        width, height = img.shape[:2]
        if success:
            output.write(img)
        cv2.imshow("output", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
