from classes.trackbars import Trackbars
from classes.camera import Camera
from classes.inklinometer import Inklinometer
from utils.config import options_dict
import cv2

trackbars = Trackbars("data/data.json")
camera = Camera("output_video2.avi")
name_of_window = "Test"
inklinometer = Inklinometer(camera=camera, trackbars=trackbars, options=options_dict)

while True:

    success, img = camera.get_image()
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, img)


    inklinometer.main()
    trackbars.save()

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
