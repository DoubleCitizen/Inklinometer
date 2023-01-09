import cv2
import numpy as np
from utils.config import *


def get_second_method(x1=0, y1=0, x2=0, y2=0, is_vert=1, count_sec=0, width_win=0, height_win=0):
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
    center = 0
    reference_point = 0
    result_second = 0
    if is_vert == 0:
        center = (y1 + y2) / 2
        reference_point = height_win / 2
    else:
        center = (x1 + x2) / 2
        reference_point = width_win / 2
    result_second = (reference_point - center) * count_sec
    print(f"reference_point = {reference_point}")
    print(f"center = {center}")
    # result_second = result_second
    return result_second


def get_resize_picture(src, scale):
    width = int(src.shape[1] * scale / 100)
    height = int(src.shape[0] * scale / 100)

    dsize = (width, height)
    return dsize


def draw_image(src, description, scale=100):
    src = cv2.resize(src, get_resize_picture(src, scale))
    cv2.imshow(description, src)


def get_cont(img, from_=200, to_=6000):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for id, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > from_ and area < to_:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return x, y, x + w, y + h


def selection_method(image, r=215, g=236, b=241, scale=100, hsv=[0, 255, 56, 255, 0, 255], med=0):
    # image = cv2.resize(image, get_resize_picture(image, scale))

    lower = np.array((hsv[0], hsv[2], hsv[4]), np.uint8)
    upper = np.array((hsv[1], hsv[3], hsv[5]), np.uint8)

    # Применение Медианного фильтра
    MedianNeChet = med
    if med > 1:
        if med % 2 == 0:
            MedianNeChet += 1
        image = cv2.medianBlur(image, MedianNeChet)

    draw_image(image, "Original", scale)

    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    draw_image(hsv_img, "hsv_img1", scale)  ## 1
    # lower = np.array([188, 199, 219])
    # upper = np.array([208, 219, 241])
    curr_mask = cv2.inRange(hsv_img, lower, upper)
    # hsv_img[curr_mask > 0] = ([208, 255, 200])
    hsv_img[curr_mask > 0] = ([255, 255, 255])
    draw_image(hsv_img, "hsv_img", scale)  ## 2

    # Фильтрация
    ## Преобразование HSV-изображения к оттенкам серого для дальнейшего
    ## оконтуривания
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

    draw_image(gray, "grayS", scale)  ## 3

    # Обрезка
    w, h = gray.shape[:2]
    thresh = cv2.inRange(hsv_img, lower, upper)
    # x1, y1, x2, y2 = get_cont(thresh, 1000, (w * h) * 0.9)
    x1, y1, x2, y2 = 0, 115, 640, 210
    cv2.rectangle(thresh, (x1, y1), (x2, y2), (0, 255, 0), 2)
    draw_image(thresh, "Test", scale)
    gray = gray[y1:y2, x1:x2]
    image = image[y1:y2, x1:x2]

    # Подсчёт th bth
    wei, hei = gray.shape[:2]

    ret, threshold = cv2.threshold(gray, r, g, b)
    draw_image(threshold, "threshold", scale)  ## 4
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # try:
    x1, y1, x2, y2 = get_cont(threshold)
    cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # except:
    #    x1, y1, x2, y2 = 0, 0, 0, 0

    cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    draw_image(image, "image", scale)  ## 5
    return x1, y1, x2, y2, gray


def GetRangeToHatch(h):
    otvet = h / REL_FROM_CENTER_TO_FIRST_HATCH
    return otvet


def GetRangeBetweenHatch(h):
    y = GetRangeToHatch(h)
    otvet = (h - y) / REL_BETWEEN_HATCH_TO_END
    # print(f"otvet = (h - y) / Rel_between_hatch_to_end")
    # print(f"{otvet} = ({h} - {y}) / {Rel_between_hatch_to_end}")
    return otvet
