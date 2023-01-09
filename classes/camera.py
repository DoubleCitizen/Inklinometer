import cv2
import numpy as np


class Camera:
    def __init__(self, source: str | int):
        self.source: str | int = source
        self.cap = cv2.VideoCapture(self.source)
        self.winfo = np.zeros((512, 512, 3), np.uint8)

    def get_image(self):
        success, img = self.cap.read()
        if not success:
            self.cap = cv2.VideoCapture(self.source)
            success, img = self.cap.read()
            return success, img
        return success, img
