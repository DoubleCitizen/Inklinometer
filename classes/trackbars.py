import json
from json import JSONDecodeError

import cv2

def back(*args):
    pass

class Trackbars:
    def empty(self, a):
        pass

    def load_json(self, path):
        try:
            with open(path, "r") as file:
                self.data = file.read()
            self.data = json.loads(self.data)
        except JSONDecodeError:
            self.data = {}

    def __init__(self, path_data):
        self.data = {}
        self.load_json(path_data)
        self.h_minT = self.data.get('h_min', 0)
        self.h_maxT = self.data.get('h_max', 255)
        self.s_minT = self.data.get('s_min', 56)
        self.s_maxT = self.data.get('s_max', 255)
        self.v_minT = self.data.get('v_min', 0)
        self.v_maxT = self.data.get('v_max', 255)
        self.w_2_leftT = self.data.get('w_2_left')
        self.w_1_rightT = self.data.get('w_1_right')
        self.rT = self.data.get('r', 215)
        self.gT = self.data.get('g', 236)
        self.bT = self.data.get('b', 241)
        self.medT = self.data.get('med', 4)
        self.horizontal_countT = self.data.get('horizontal_count', 1)
        self.height_1T = self.data.get('height_1')
        self.height_2T = self.data.get('height_2')
        self.width_1T = self.data.get('width_1')
        self.width_2T = self.data.get('width_2')
        self.scale_percentT = self.data.get('scale_percent', 100)

        cv2.namedWindow("NewMethod")
        cv2.resizeWindow("NewMethod", 640, 240)
        cv2.createTrackbar("Red", "NewMethod", 0, 255, self.empty)
        cv2.createTrackbar("Green", "NewMethod", 0, 255, self.empty)
        cv2.createTrackbar("Blue", "NewMethod", 0, 255, self.empty)
        cv2.createTrackbar("Median", "NewMethod", 0, 10, self.empty)


        cv2.namedWindow("Rotate Images")
        cv2.resizeWindow("Rotate Images", 600, 100)
        cv2.createTrackbar("Rotate Angle", "Rotate Images", 0, 360, self.empty)
        cv2.createTrackbar("Horizontal Counting", "Rotate Images", 0, 1, self.empty)

        cv2.namedWindow("Rectangles")
        cv2.resizeWindow("Rectangles", 600, 200)
        cv2.createTrackbar("Left Rect", "Rectangles", 0, 400, self.empty)
        cv2.createTrackbar("Right Rect", "Rectangles", 0, 400, self.empty)

        cv2.namedWindow("TrackBarsSize")
        cv2.resizeWindow("TrackBarsSize", 680, 240)
        cv2.createTrackbar("Height Start", "TrackBarsSize", 0, 1080 * 2, self.empty)
        cv2.createTrackbar("Height End", "TrackBarsSize", 0, 1080 * 2, self.empty)
        cv2.createTrackbar("width Start", "TrackBarsSize", 0, 1920 * 2, self.empty)
        cv2.createTrackbar("width End", "TrackBarsSize", 0, 1920 * 2, self.empty)
        cv2.createTrackbar("Scale Percent", "TrackBarsSize", 20, 100, self.empty)

        cv2.namedWindow("HSV New Method")
        cv2.resizeWindow("HSV New Method", 640, 300)
        cv2.createTrackbar("H Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("H Max", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("S Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("S Max", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("V Min", "HSV New Method", 0, 255, self.empty)
        cv2.createTrackbar("V Max", "HSV New Method", 0, 255, self.empty)

        cv2.setTrackbarPos("H Min", "HSV New Method", self.h_minT)
        cv2.setTrackbarPos("H Max", "HSV New Method", self.h_maxT)
        cv2.setTrackbarPos("S Min", "HSV New Method", self.s_minT)
        cv2.setTrackbarPos("S Max", "HSV New Method", self.s_maxT)
        cv2.setTrackbarPos("V Min", "HSV New Method", self.v_minT)
        cv2.setTrackbarPos("V Max", "HSV New Method", self.v_maxT)

        cv2.setTrackbarPos("Left Rect", "Rectangles", self.w_2_leftT)
        cv2.setTrackbarPos("Right Rect", "Rectangles", self.w_1_rightT)

        cv2.setTrackbarPos("Red", "NewMethod", self.rT)
        cv2.setTrackbarPos("Green", "NewMethod", self.gT)
        cv2.setTrackbarPos("Blue", "NewMethod", self.bT)
        cv2.setTrackbarPos("Median", "NewMethod", self.medT)

        cv2.setTrackbarPos("Horizontal Counting", "Rotate Images", self.horizontal_countT)

        cv2.setTrackbarPos("Height Start", "TrackBarsSize", self.height_1T)
        cv2.setTrackbarPos("Height End", "TrackBarsSize", self.height_2T)
        cv2.setTrackbarPos("width Start", "TrackBarsSize", self.width_1T)
        cv2.setTrackbarPos("width End", "TrackBarsSize", self.width_2T)

        cv2.setTrackbarPos("Scale Percent", "TrackBarsSize", self.scale_percentT)

    def save(self):
        data = {
            "r": self.r,
            "g": self.g,
            "b": self.b,
            "med": self.med,
            "h_min": self.h_min,
            "h_max": self.h_max,
            "s_min": self.s_min,
            "s_max": self.s_max,
            "v_min": self.v_min,
            "v_max": self.v_max,
            "w_2_left": self.w_2_left,
            "w_1_right": self.w_1_right,
            "horizontal_count": self.horizontal_count,
            "height_1": self.height_1,
            "height_2": self.height_2,
            "width_1": self.width_1,
            "width_2": self.width_2,
            "scale_percent": self.scale_percent,
        }
        with open("data/data.json", "w") as file:
            file.write(json.dumps(data))

    @property
    def r(self):
        r = cv2.getTrackbarPos("Red", "NewMethod")
        return r

    @property
    def g(self):
        g = cv2.getTrackbarPos("Green", "NewMethod")
        return g

    @property
    def b(self):
        b = cv2.getTrackbarPos("Blue", "NewMethod")
        return b

    @property
    def med(self):
        med = cv2.getTrackbarPos("Median", "NewMethod")
        return med

    @property
    def h_min(self):
        h_min = cv2.getTrackbarPos("H Min", "HSV New Method")
        return h_min

    @property
    def h_max(self):
        h_max = cv2.getTrackbarPos("H Max", "HSV New Method")
        return h_max

    @property
    def s_min(self):
        s_min = cv2.getTrackbarPos("S Min", "HSV New Method")
        return s_min

    @property
    def s_max(self):
        s_max = cv2.getTrackbarPos("S Max", "HSV New Method")
        return s_max

    @property
    def v_min(self):
        v_min = cv2.getTrackbarPos("V Min", "HSV New Method")
        return v_min

    @property
    def v_max(self):
        v_max = cv2.getTrackbarPos("V Max", "HSV New Method")
        return v_max

    @property
    def ang(self):
        ang = cv2.getTrackbarPos("Rotate Angle", "Rotate Images")
        return ang

    @property
    def horizontal_count(self):
        horizontal_count = cv2.getTrackbarPos("Horizontal Counting", "Rotate Images")
        return horizontal_count

    @property
    def height_1(self):
        height_1 = cv2.getTrackbarPos("Height Start", "TrackBarsSize")
        return height_1

    @property
    def height_2(self):
        height_2 = cv2.getTrackbarPos("Height End", "TrackBarsSize")
        return height_2

    @property
    def width_1(self):
        width_1 = cv2.getTrackbarPos("width Start", "TrackBarsSize")
        return width_1

    @property
    def width_2(self):
        width_2 = cv2.getTrackbarPos("width End", "TrackBarsSize")
        return width_2

    @property
    def scale_percent(self):
        scale_percent = cv2.getTrackbarPos("Scale Percent", "TrackBarsSize")
        return scale_percent

    @property
    def w_2_left(self):
        w_2_left = cv2.getTrackbarPos("Left Rect", "Rectangles")
        return w_2_left

    @property
    def w_1_right(self):
        w_1_right = cv2.getTrackbarPos("Right Rect", "Rectangles")
        return w_1_right

    @h_min.setter
    def h_min(self, value):
        self._h_min = value

    @h_max.setter
    def h_max(self, value):
        self._h_max = value

    @s_min.setter
    def s_min(self, value):
        self._s_min = value

    @s_max.setter
    def s_max(self, value):
        self._s_max = value

    @v_min.setter
    def v_min(self, value):
        self._v_min = value

    @v_max.setter
    def v_max(self, value):
        self._v_max = value

    @r.setter
    def r(self, value):
        self._r = value

    @g.setter
    def g(self, value):
        self._g = value

    @b.setter
    def b(self, value):
        self._b = value

    @med.setter
    def med(self, value):
        self._med = value
