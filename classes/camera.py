import cv2
import numpy as np


class Camera:
    def __init__(self, source: str | int):
        self.count_frames = 0
        self.source: str | int = source
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
        self.winfo = np.zeros((512, 512, 3), np.uint8)

    def get_image(self):
        success, img = self.cap.read()
        self.count_frames += 1
        if not success:
            self.cap = cv2.VideoCapture(self.source)
            success, img = self.cap.read()
            return success, img
        return success, img

    def get_fps(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return fps

    def get_frames(self):
        return self.count_frames

    def get_all_frames(self):
        length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return length
