from datetime import datetime, timedelta

from classes.camera import Camera
from classes.convert_file_txt_to_dict2 import ConverterTxtToDict
import cv2

from classes.read_file import ReaderTxt

camera = Camera(1)

converter_txt_to_dict = ConverterTxtToDict()

success, img = camera.get_image()
height, width = (640, 480)

path = "data"

datetime_now_inklinometer = str(datetime.now().replace(microsecond=0) - timedelta(seconds=0))
datetime_now_inklinometer = datetime_now_inklinometer.replace('-', '_')
datetime_now_inklinometer = datetime_now_inklinometer.replace(':', '_')
datetime_now_inklinometer = datetime_now_inklinometer.replace(' ', '_')

output = cv2.VideoWriter(f'{path}/inklin_{datetime_now_inklinometer}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (height, width))

reader_txt = ReaderTxt("data/data_port_spy_2.txt")


while True:

    success, img = camera.get_image()
    height, width = img.shape[:2]

    # data = converter_txt_to_dict.convert(data=reader_txt.read())

    output.write(img)
    cv2.imshow("output", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
output.release()
camera.cap.release()

