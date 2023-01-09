import cv2
import numpy as np

from classes.camera import Camera
from classes.trackbars import Trackbars


class Inklinometer:
    def __init__(self, camera: Camera, trackbars: Trackbars, options: dict):
        self.gray = None
        self.REL_FROM_CENTER_TO_FIRST_HATCH = options["REL_FROM_CENTER_TO_FIRST_HATCH"]
        self.REL_BETWEEN_HATCH_TO_END = options["REL_BETWEEN_HATCH_TO_END"]
        self.NUMBER_OF_ARC_SECONDS_ONE_STROKE = options["NUMBER_OF_ARC_SECONDS_ONE_STROKE"]
        self.COUNT_ARC_SECOND = options["COUNT_ARC_SECOND"]
        self.camera = camera
        self.trackbars = trackbars
        success, img = camera.get_image()
        self.height, self.width = img.shape[:2]
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.is_vert = 0
        self.getgrad = "NONE"
        self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing = 0, 0, 0, 0

    def get_second_method(self):
        """
        Функция определяет сколько в одном пикселе угловых секунд
        И выводит результат
        :param x1: координата пузырька
        :param y1: координата пузырька
        :param x2: координата пузырька
        :param y2: координата пузырька
        :param is_vert: булевское значение повернутости экрана
        :param count_sec: Количество секунд в одном пикселе
        :param width_win: ширина окна
        :param height_win: высота окна
        :return: Возрвращает угловые секунды
        """
        if self.is_vert == 0:
            center = (self.y1 + self.y2) / 2
            reference_point = self.height / 2
        else:
            center = (self.x1 + self.x2) / 2
            reference_point = self.width / 2
        result_second = (reference_point - center) * self.COUNT_ARC_SECOND
        # print(f"reference_point = {reference_point}")
        # print(f"center = {center}")
        return result_second

    def view_image(self, src, str, scale=100):
        try:
            src = cv2.resize(src, self.get_resize_picture(src, scale))
            cv2.imshow(str, src)
        except:
            pass

    def get_cont(self, img, from_=200, to_=6000):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = 0, 0, 0, 0
        for id, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > from_ and area < to_:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)

        # Переменные для того чтобы повторно не проводить обрезку
        area_framing = abs(self.x2_framing - self.x1_framing) * abs(self.y2_framing - self.y1_framing) - (w + h)

        # self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing = 0, 0, 0, 0
        if abs(self.x1_framing - x) + abs(self.x2_framing - (x + w)) + abs(self.y1_framing - y) + abs(
                self.y2_framing - (y + h)) > 10 * 4 or area_framing > 100000:
            return x, y, x + w, y + h
        else:
            return self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing

    def select_method(self, image, r=215, g=236, b=241, scale=100, hsv=[0, 255, 56, 255, 0, 255], med=0):
        # image = cv2.resize(image, get_resize_picture(image, scale))

        lower = np.array((hsv[0], hsv[2], hsv[4]), np.uint8)
        upper = np.array((hsv[1], hsv[3], hsv[5]), np.uint8)

        # Применение Медианного фильтра
        MedianNeChet = med
        if med > 1:
            if med % 2 == 0:
                MedianNeChet += 1
            image = cv2.medianBlur(image, MedianNeChet)

        self.view_image(image, "Original", scale)
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # lower = np.array([188, 199, 219])
        # upper = np.array([208, 219, 241])
        curr_mask = cv2.inRange(hsv_img, lower, upper)
        # hsv_img[curr_mask > 0] = ([208, 255, 200])
        hsv_img[curr_mask > 0] = ([255, 255, 255])
        self.view_image(hsv_img, "hsv_img", scale)  ## 2

        # Фильтрация
        ## Преобразование HSV-изображения к оттенкам серого для дальнейшего
        ## оконтуривания
        RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
        self.gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

        # Обрезка
        w, h = self.gray.shape[:2]
        thresh = cv2.inRange(hsv_img, lower, upper)
        self.x1_framing, self.y1_framing, self.x2_framing, self.y2_framing = self.get_cont(thresh, 1000, (w * h) * 0.9)
        # x1, y1, x2, y2 = 0, 115, 640, 210
        cv2.rectangle(thresh, (self.x1_framing, self.y1_framing), (self.x2_framing, self.y2_framing), (0, 255, 0), 2)
        self.view_image(thresh, "Test", scale)
        self.gray = self.gray[self.y1_framing:self.y2_framing, self.x1_framing:self.x2_framing]
        image = image[self.y1_framing:self.y2_framing, self.x1_framing:self.x2_framing]

        ret, threshold = cv2.threshold(self.gray, r, g, b)
        self.view_image(threshold, "threshold", scale)  ## 4
        contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        x1, y1, x2, y2 = self.get_cont(threshold)
        cv2.rectangle(self.gray, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        self.view_image(image, "image", scale)  ## 5
        return x1, y1, x2, y2

    @staticmethod
    def get_resize_picture(src, scale):
        width = int(src.shape[1] * scale / 100)
        height = int(src.shape[0] * scale / 100)

        dsize = (width, height)
        return dsize

    @property
    def th(self) -> int | float:
        horizontal_count = self.trackbars.horizontal_count
        if horizontal_count == 0:
            th = (self.height // 2) / self.REL_FROM_CENTER_TO_FIRST_HATCH
        else:
            th = (self.width // 2) / self.REL_FROM_CENTER_TO_FIRST_HATCH
        return th

    @property
    def bth(self) -> int | float:
        horizontal_count = self.trackbars.horizontal_count
        if horizontal_count == 0:
            bth = ((self.height // 2) - self.th) / self.REL_BETWEEN_HATCH_TO_END
        else:
            bth = ((self.width // 2) - self.th) / self.REL_BETWEEN_HATCH_TO_END
        return bth

    @property
    def get_gradus(self):
        # Штрихи
        horizontal_count = self.trackbars.horizontal_count
        y_ex = self.extreme_values(self.y1, self.y2, self.height / 2)
        x_ex = self.extreme_values(self.x1, self.x2, self.width / 2)
        if horizontal_count == 0:
            center = self.height // 2
            ex = y_ex
        else:
            center = self.width // 2
            ex = x_ex

        diap1 = [self.th, self.th + self.bth * 8]
        diap2 = [-self.th, -self.th - self.bth * 8]
        centerDiap = self.th + (self.bth * 8) / 2
        ex -= center
        if horizontal_count == 0:
            cv2.rectangle(self.gray, ((self.width), round(self.th + center)),
                          ((self.width), round(centerDiap + center)),
                          (0, 255, 0),
                          1)
            cv2.rectangle(self.gray, ((self.width), round(-self.th + center)),
                          ((self.width), round(-centerDiap + center)),
                          (0, 255, 0),
                          1)
        else:
            cv2.rectangle(self.gray, (round(self.th + center), (self.width)),
                          (round(centerDiap + center), (self.width)),
                          (0, 255, 0),
                          1)
            cv2.rectangle(self.gray, (round(-self.th + center), (self.width)),
                          (round(-centerDiap + center), (self.width)),
                          (0, 255, 0),
                          1)
        if ex >= diap1[0] and ex <= diap1[1]:
            self.getgrad = -(centerDiap - ex)
            self.getgrad = (self.getgrad / self.bth) * self.NUMBER_OF_ARC_SECONDS_ONE_STROKE
            self.getgrad = round(self.getgrad, 2)
            if self.getgrad < 0:
                self.getgrad = "~=0"
        elif ex >= diap2[1] and ex <= diap2[0]:
            self.getgrad = -(-centerDiap - ex)
            self.getgrad = (self.getgrad / self.bth) * self.NUMBER_OF_ARC_SECONDS_ONE_STROKE
            self.getgrad = round(self.getgrad, 2)
            if self.getgrad > 0:
                self.getgrad = "~=0"
        else:
            self.getgrad = "NONE"

        maxgrad = self.COUNT_ARC_SECOND * 4
        if horizontal_count == 0:
            if self.getgrad == "NONE":
                self.getgrad = self.getgrad
            elif self.getgrad == ">" + str(maxgrad):
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = ">" + str(maxgrad)
            elif self.getgrad == "<-" + str(maxgrad):
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = "<-" + str(maxgrad)
            elif self.getgrad == "~=0":
                self.getgrad = self.getgrad
            elif self.getgrad > 0:
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = ">" + str(maxgrad)
            elif self.getgrad <= 0:
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = "<-" + str(maxgrad)
        else:
            if self.getgrad == "NONE":
                self.getgrad = self.getgrad
            elif self.getgrad == ">" + str(maxgrad):
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = ">" + str(maxgrad)
            elif self.getgrad == "<-" + str(maxgrad):
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = "<-" + str(maxgrad)
            elif self.getgrad == "~=0":
                self.getgrad = self.getgrad
            elif self.getgrad > 0:
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = ">" + str(maxgrad)
            elif self.getgrad <= 0:
                self.getgrad = self.getgrad
                if self.getgrad == "NONE":
                    self.getgrad = "<-" + str(maxgrad)

        return self.getgrad

    @staticmethod
    def extreme_values(y_up, y_down, center):
        if (y_up + y_down) / 2 < center:
            return y_up
        else:
            return y_down

    def main(self):
        r = self.trackbars.r
        g = self.trackbars.g
        b = self.trackbars.b
        med = self.trackbars.med

        h_min = self.trackbars.h_min
        h_max = self.trackbars.h_max
        s_min = self.trackbars.s_min
        s_max = self.trackbars.s_max
        v_min = self.trackbars.v_min
        v_max = self.trackbars.v_max
        hsv_list = [h_min, h_max, s_min, s_max, v_min, v_max]

        success, img = self.camera.get_image()

        horizontal_count = self.trackbars.horizontal_count

        x_ex = self.extreme_values(self.x1, self.x2, self.width / 2)

        scale_percent = self.trackbars.scale_percent
        if scale_percent == 0:
            scale_percent = 1

        # Подсчёт значений по x, y
        self.x1, self.y2, self.x2, self.y1 = self.select_method(img, r=r, g=g, b=b, scale=scale_percent, hsv=hsv_list,
                                                                med=med)
        self.height, self.width = img.shape[:2]

        th = self.th
        bth = self.bth

        # Центральная линия
        if horizontal_count == 0:
            # Штрихи
            cv2.rectangle(self.gray, (0, round(th + self.height / 2)),
                          (self.width, round(th + bth * 8 + self.height / 2)),
                          (0, 255, 0), 4)
            cv2.rectangle(self.gray, (0, round(self.height / 2 - th)),
                          (self.width, round(self.height / 2 - th - bth * 8)),
                          (0, 255, 0), 4)

            # Центральная линия
            # cv2.rectangle(imgContour, (0,((self.height)//2)), (1920,((self.height)//2)), (0,255,0), 6)
            cv2.rectangle(self.gray, (0, (self.height // 2)), (1920, (self.height // 2)), (0, 255, 0), 6)
        else:
            # Штрихи
            cv2.rectangle(self.gray, (round(th + self.width / 2), 0),
                          (round(th + bth * 8 + self.width / 2), self.height),
                          (0, 255, 0),
                          4)
            cv2.rectangle(self.gray, (round(self.width / 2 - th), 0),
                          (round(self.width / 2 - th - bth * 8), self.height),
                          (0, 255, 0),
                          4)

            # Центральная линия
            cv2.rectangle(self.gray, ((self.width // 2), 0), ((self.width // 2), 1920), (0, 255, 0), 6)
            cv2.rectangle(self.gray, ((self.width // 2), 0), ((self.width // 2), 1920), (0, 255, 0), 6)

            # Заполнение информационного окна
            winfo = np.zeros((512, 512, 3), np.uint8)
            cv2.putText(winfo, f"Отклонение пузырька = {self.get_gradus}''", (0, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
            cv2.putText(winfo, f"X_EX = {x_ex}px", (0, 200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.putText(winfo, f"Center = {self.width / 2}px", (0, 250), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.putText(winfo, f"X_left = {self.x1}px", (0, 300), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.putText(winfo, f"X_right = {self.x2}px", (0, 350), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.putText(winfo, f"SR_arifm = {(self.x1 + self.x2) / 2}px", (0, 400), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 150, 0),
                        2)
            cv2.putText(winfo, f"bth = {bth}px", (0, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.putText(winfo,
                        f"count_sec = {self.get_second_method()}''",
                        (0, 500), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)

            # Отображение изображений
            self.view_image(self.gray, "gray", scale_percent)  ## 3
            cv2.putText(winfo,
                        f"count_sec = {self.get_second_method()}''",
                        (0, 500), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
            cv2.imshow("Window", winfo)
