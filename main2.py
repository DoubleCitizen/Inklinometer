import cv2
import numpy as np
import math
import datetime
import imutils
import os
import threading

from PIL import Image, ImageEnhance

# path = "Resources/IMG_21.mov"
# path = "Resources/normal/IMG_6050.mov"

# path = "Resources/Fresh/IMG_6306.mov"
#path = "output_video3.avi"
path = 0
# cap = cv2.VideoCapture('http://192.168.1.49:81/stream')
cap = cv2.VideoCapture(path)
winfo = np.zeros((512, 512, 3), np.uint8)

mwei, mhei = 0, 0

global Rel_from_center_to_first_hatch, Rel_between_hatch_to_end, countSec, getgrad
getgrad = "NONE"
Rel_from_center_to_first_hatch = 40 / 8.5
Rel_between_hatch_to_end = 31.5 / 2
countSec = 4


def empty(a):
    pass


cv2.namedWindow("Rotate Images")
cv2.resizeWindow("Rotate Images", 600, 100)
cv2.createTrackbar("Rotate Angle", "Rotate Images", 0, 360, empty)
cv2.createTrackbar("Horizontal Counting", "Rotate Images", 0, 1, empty)

cv2.namedWindow("Rectangles")
cv2.resizeWindow("Rectangles", 600, 200)
cv2.createTrackbar("Left Rect", "Rectangles", 0, 400, empty)
cv2.createTrackbar("Right Rect", "Rectangles", 0, 400, empty)

cv2.namedWindow("TrackBarsSize")
cv2.resizeWindow("TrackBarsSize", 680, 240)
cv2.createTrackbar("Height Start", "TrackBarsSize", 0, 1080 * 2, empty)
cv2.createTrackbar("Height End", "TrackBarsSize", 0, 1080 * 2, empty)
cv2.createTrackbar("Weight Start", "TrackBarsSize", 0, 1920 * 2, empty)
cv2.createTrackbar("Weight End", "TrackBarsSize", 0, 1920 * 2, empty)
cv2.createTrackbar("Scale Percent", "TrackBarsSize", 20, 100, empty)

# height_1T = 0
# height_2T = 100
# weight_1T = 0
# weight_2T = 100
y_arr = []
h_arr = []
y_up = 0
y_down = 0
x_left = 0
x_right = 0

SKO = 4

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
    #result_second = result_second
    return result_second


def viewImage(src, str, scale=100):
    try:
        src = cv2.resize(src, Get_ResizePicture(src, scale))
        cv2.imshow(str, src)
    except:
        pass


def getCont(img, from_=200, to_=6000):
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


def SelectMethod(image, r=215, g=236, b=241, scale=100, hsv=[0, 255, 56, 255, 0, 255], med=0):
    # image = cv2.resize(image, Get_ResizePicture(image, scale))

    lower = np.array((hsv[0], hsv[2], hsv[4]), np.uint8)
    upper = np.array((hsv[1], hsv[3], hsv[5]), np.uint8)

    # Применение Медианного фильтра
    MedianNeChet = med
    if med > 1:
        if med % 2 == 0:
            MedianNeChet += 1
        image = cv2.medianBlur(image, MedianNeChet)

    viewImage(image, "Original", scale)

    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    viewImage(hsv_img, "hsv_img1", scale)  ## 1
    # lower = np.array([188, 199, 219])
    # upper = np.array([208, 219, 241])
    curr_mask = cv2.inRange(hsv_img, lower, upper)
    # hsv_img[curr_mask > 0] = ([208, 255, 200])
    hsv_img[curr_mask > 0] = ([255, 255, 255])
    viewImage(hsv_img, "hsv_img", scale)  ## 2

    # Фильтрация
    ## Преобразование HSV-изображения к оттенкам серого для дальнейшего
    ## оконтуривания
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

    viewImage(gray, "grayS", scale)  ## 3

    # Обрезка
    w, h = gray.shape[:2]
    thresh = cv2.inRange(hsv_img, lower, upper)
    #x1, y1, x2, y2 = getCont(thresh, 1000, (w * h) * 0.9)
    x1, y1, x2, y2 = 0, 115, 640, 210
    cv2.rectangle(thresh, (x1, y1), (x2, y2), (0, 255, 0), 2)
    viewImage(thresh, "Test", scale)
    gray = gray[y1:y2, x1:x2]
    image = image[y1:y2, x1:x2]

    # Подсчёт th bth
    wei, hei = gray.shape[:2]

    ret, threshold = cv2.threshold(gray, r, g, b)
    viewImage(threshold, "threshold", scale)  ## 4
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #try:
    x1, y1, x2, y2 = getCont(threshold)
    cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #except:
    #    x1, y1, x2, y2 = 0, 0, 0, 0

    cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    viewImage(image, "image", scale)  ## 5
    return x1, y1, x2, y2, gray


def Get_ResizePicture(src, scale):
    width = int(src.shape[1] * scale / 100)
    height = int(src.shape[0] * scale / 100)

    dsize = (width, height)
    return dsize


def CreateTxt(mes, h, m, s, ms):
    if mes != "NONE":
        string = "@Python " + str(h) + " " + str(m) + " " + str(s) + " " + str(ms) + " " + str(mes) + "\n"
        # string = "@Python " + str(mes) + "\n"

        with open("hello.txt", "a+") as file:
            file.write(string)


def GetRangeToHatch(h):
    otvet = h / Rel_from_center_to_first_hatch
    return otvet


def GetRangeBetweenHatch(h):
    y = GetRangeToHatch(h)
    otvet = (h - y) / Rel_between_hatch_to_end
    # print(f"otvet = (h - y) / Rel_between_hatch_to_end")
    # print(f"{otvet} = ({h} - {y}) / {Rel_between_hatch_to_end}")
    return otvet


def GetGradus(th, bth, y, center, horiz_c):
    # Штрихи
    # cv2.rectangle(gray, ((0),round(th+height_y/2)),((weight_x),round(th+bth*8+height_y/2)),(0,255,0),4)
    # cv2.rectangle(gray, ((0),round(height_y/2-th)),((weight_x),round(height_y/2-th-bth*8)),(0,255,0),4)
    # Центральная линия
    # cv2.rectangle(imgContour, (0,((height_y)//2)), (1920,((height_y)//2)), (0,255,0), 6)
    # cv2.rectangle(gray, (0,((height_y)//2)), (1920,((height_y)//2)), (0,255,0), 6)

    diap1 = [th, th + bth * 8]
    diap2 = [-th, -th - bth * 8]
    centerDiap = th + (bth * 8) / 2
    # print("=======")
    # print(f"y_ex(y) = {y}")
    y -= center
    # print(f"y - center = {y}")
    # print(f"centerDiap = {centerDiap}")
    # print(f"diap1 = {diap1}")
    # print(f"diap2 = {diap2}")
    if horiz_c == 0:
        cv2.rectangle(gray, ((weight_x), round(th + center)), ((weight_x), round(centerDiap + center)), (0, 255, 0), 1)
        cv2.rectangle(gray, ((weight_x), round(-th + center)), ((weight_x), round(-centerDiap + center)), (0, 255, 0),
                      1)
    else:
        cv2.rectangle(gray, (round(th + center), (weight_x)), (round(centerDiap + center), (weight_x)), (0, 255, 0), 1)
        cv2.rectangle(gray, (round(-th + center), (weight_x)), (round(-centerDiap + center), (weight_x)), (0, 255, 0),
                      1)
    if y >= diap1[0] and y <= diap1[1]:
        second = -(centerDiap - y)
        second = (second / bth) * countSec
        second = round(second, 2)
        if second < 0:
            second = "~=0"
    elif y >= diap2[1] and y <= diap2[0]:
        second = -(-centerDiap - y)
        second = (second / bth) * countSec
        second = round(second, 2)
        if second > 0:
            second = "~=0"
    else:
        second = "NONE"
    return second


def Extreme_Values(y_up, y_down, center):
    if (y_up + y_down) / 2 < center:
        return y_up
    else:
        return y_down


# Среднее арифметическое
def Aver_Arif(arr):
    sum = 0
    for id, val in enumerate(arr):
        sum += val
    return sum / len(arr)


# Отклонение
def Deviation(arr, aver):
    dev_arr = []
    for id, val in enumerate(arr):
        dev_arr.append(aver - val)
    return dev_arr


# СКП
def SKP(arr):
    sumkv = 0
    n = len(arr) - 1
    if n <= 0:
        n = 1
    for id, val in enumerate(arr):
        sumkv += val * val
    return math.sqrt((sumkv) / (n))


# Исключение аномальных погрешностей
def exception_anomalies(skp, sko, arr):
    arrnew = arr.copy()
    arrnew = arrnew.sort()
    try:
        while skp > sko or len(arrnew) <= 1:
            arrnew.pop()
        return arrnew
    except:
        return arr


# писание файла Readme
with open("Readme.txt", "w") as file:
    file.write("Для настроек параметров уровня, редактируйте файл options.txt\n")
    file.write("В данном файле переменные измеряются в мм")
    file.write("")

arr_data_yroven = []

with open("options.txt", "r+") as file:
    i = 0
    for line in file:
        string = str(line)

        string = string[string.find("=") + 2:len(string)]

        arr_data_yroven.append(float(string))
        i = i + 1
    if i == 0:
        file.write("Расстояние между штрихами = 2\n")
        file.write("Длина колбы делённое на два = 40\n")
        file.write("Расстояние от первого штриха до конца колбы = 31.5\n")
        file.write("Расстояние от центра колбы до первого штриха = 8.5\n")
        file.write("Количество угловых секунд на одном штрихе = 4")

Rel_from_center_to_first_hatch = arr_data_yroven[1] / arr_data_yroven[3]
Rel_between_hatch_to_end = arr_data_yroven[2] / arr_data_yroven[0]
countSec = arr_data_yroven[4]

# Rel_from_center_to_first_hatch = 40 / 8.5
# Rel_between_hatch_to_end = 31.5 / 2

try:
    data = []
    with open("data.txt", "r") as file:
        for line in file:
            data.append(line)
    for i in range(len(data)):
        string = data[i]
        data[i] = string[0:len(string) - 1]
except:
    pass

# Кропы (ну ты понял)
height_1T = 120
height_2T = 1016
weight_1T = 440
weight_2T = 540

scale_percentT = 50
horizontal_countT = 0

# Настройки которые ты крутил обычно (ну ты понял, да?)
h_minT, h_maxT, s_minT, s_maxT, v_minT, v_maxT = 0, 255, 0, 96, 130, 255
h2_minT, h2_maxT, s2_minT, s2_maxT, v2_minT, v2_maxT = 0, 255, 0, 96, 130, 255
h_min_nmT, h_max_nmT, s_min_nmT, s_max_nmT, v_min_nmT, v_max_nmT = 73, 255, 75, 255, 0, 255
rT, gT, bT, mT = 215, 240, 241, 0
angT = 0
FilterKernelT = 1
FilterKernelT2 = 1
MedianT2 = 1

try:
    angT = int(data[0])
    h_minT = int(data[1])
    h_maxT = int(data[2])
    s_minT = int(data[3])
    s_maxT = int(data[4])
    v_minT = int(data[5])
    v_maxT = int(data[6])
    height_1T = int(data[7])
    height_2T = int(data[8])
    weight_1T = int(data[9])
    weight_2T = int(data[10])
    scale_percentT = int(data[11])
    h2_minT = int(data[12])
    h2_maxT = int(data[13])
    s2_minT = int(data[14])
    s2_maxT = int(data[15])
    v2_minT = int(data[16])
    v2_maxT = int(data[17])
    FilterKernelT = int(data[18])
    FilterKernelT2 = int(data[19])
    MedianT2 = int(data[20])
    horizontal_countT = int(data[21])
    h_min_nmT = int(data[22])
    h_max_nmT = int(data[23])
    s_min_nmT = int(data[24])
    s_max_nmT = int(data[25])
    v_min_nmT = int(data[26])
    v_max_nmT = int(data[27])
    rT = int(data[28])
    gT = int(data[29])
    bT = int(data[30])
    mT = int(data[31])
except:
    # print("NULL Data.txt")
    try:
        os.remove("data.txt")
    except:
        pass
    with open("data.txt", "w") as file:
        file.write(str(angT) + "\n")

        file.write(str(h_minT) + "\n")
        file.write(str(h_maxT) + "\n")
        file.write(str(s_minT) + "\n")
        file.write(str(s_maxT) + "\n")
        file.write(str(v_minT) + "\n")
        file.write(str(v_maxT) + "\n")

        file.write(str(height_1T) + "\n")
        file.write(str(height_2T) + "\n")
        file.write(str(weight_1T) + "\n")
        file.write(str(weight_2T) + "\n")

        file.write(str(scale_percentT) + "\n")
        file.write(str(h2_minT) + "\n")
        file.write(str(h2_maxT) + "\n")
        file.write(str(s2_minT) + "\n")
        file.write(str(s2_maxT) + "\n")
        file.write(str(v2_minT) + "\n")
        file.write(str(v2_maxT) + "\n")
        file.write(str(FilterKernelT) + "\n")
        file.write(str(FilterKernelT2) + "\n")
        file.write(str(MedianT2) + "\n")
        file.write(str(horizontal_countT) + "\n")

        file.write(str(h_min_nmT) + "\n")
        file.write(str(h_max_nmT) + "\n")
        file.write(str(s_min_nmT) + "\n")
        file.write(str(s_max_nmT) + "\n")
        file.write(str(v_min_nmT) + "\n")
        file.write(str(v_max_nmT) + "\n")

        file.write(str(rT) + "\n")
        file.write(str(gT) + "\n")
        file.write(str(bT) + "\n")
        file.write(str(mT) + "\n")

w_2_leftT = 10
w_1_rightT = 200

out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (640, 480))

ang = cv2.setTrackbarPos("Rotate Angle", "Rotate Images", angT)
horizontal_count = cv2.setTrackbarPos("Horizontal Counting", "Rotate Images", horizontal_countT)

height_1 = cv2.setTrackbarPos("Height Start", "TrackBarsSize", height_1T)
height_2 = cv2.setTrackbarPos("Height End", "TrackBarsSize", height_2T)
weight_1 = cv2.setTrackbarPos("Weight Start", "TrackBarsSize", weight_1T)
weight_2 = cv2.setTrackbarPos("Weight End", "TrackBarsSize", weight_2T)

scale_percent = cv2.setTrackbarPos("Scale Percent", "TrackBarsSize", scale_percentT)

# Трэк бары нового метода
cv2.namedWindow("NewMethod")
cv2.resizeWindow("NewMethod", 640, 240)
cv2.createTrackbar("Red", "NewMethod", 0, 255, empty)
cv2.createTrackbar("Green", "NewMethod", 0, 255, empty)
cv2.createTrackbar("Blue", "NewMethod", 0, 255, empty)
cv2.createTrackbar("Median", "NewMethod", 0, 10, empty)

red = cv2.setTrackbarPos("Red", "NewMethod", rT)
green = cv2.setTrackbarPos("Green", "NewMethod", gT)
blue = cv2.setTrackbarPos("Blue", "NewMethod", bT)
med = cv2.setTrackbarPos("Median", "NewMethod", mT)

# Трэк бары нового метода
cv2.namedWindow("HSV New Method")
cv2.resizeWindow("HSV New Method", 640, 300)
cv2.createTrackbar("H Min", "HSV New Method", 0, 255, empty)
cv2.createTrackbar("H Max", "HSV New Method", 0, 255, empty)
cv2.createTrackbar("S Min", "HSV New Method", 0, 255, empty)
cv2.createTrackbar("S Max", "HSV New Method", 0, 255, empty)
cv2.createTrackbar("V Min", "HSV New Method", 0, 255, empty)
cv2.createTrackbar("V Max", "HSV New Method", 0, 255, empty)

h_min_nm = cv2.setTrackbarPos("H Min", "HSV New Method", h_min_nmT)
h_max_nm = cv2.setTrackbarPos("H Max", "HSV New Method", h_max_nmT)
s_min_nm = cv2.setTrackbarPos("S Min", "HSV New Method", s_min_nmT)
s_max_nm = cv2.setTrackbarPos("S Max", "HSV New Method", s_max_nmT)
v_min_nm = cv2.setTrackbarPos("V Min", "HSV New Method", v_min_nmT)
v_max_nm = cv2.setTrackbarPos("V Max", "HSV New Method", v_max_nmT)

w_2_left = cv2.setTrackbarPos("Left Rect", "Rectangles", w_2_leftT)
w_1_right = cv2.setTrackbarPos("Right Rect", "Rectangles", w_1_rightT)

while (cap.isOpened()):

    r = cv2.getTrackbarPos("Red", "NewMethod")
    g = cv2.getTrackbarPos("Green", "NewMethod")
    b = cv2.getTrackbarPos("Blue", "NewMethod")
    med = cv2.getTrackbarPos("Median", "NewMethod")

    h_min_nm = cv2.getTrackbarPos("H Min", "HSV New Method")
    h_max_nm = cv2.getTrackbarPos("H Max", "HSV New Method")
    s_min_nm = cv2.getTrackbarPos("S Min", "HSV New Method")
    s_max_nm = cv2.getTrackbarPos("S Max", "HSV New Method")
    v_min_nm = cv2.getTrackbarPos("V Min", "HSV New Method")
    v_max_nm = cv2.getTrackbarPos("V Max", "HSV New Method")
    hsv_list = [h_min_nm, h_max_nm, s_min_nm, s_max_nm, v_min_nm, v_max_nm]

    try:
        success, img = cap.read()
    except:
        continue

    if success == False:
        cap = cv2.VideoCapture(path)
        success, img = cap.read()

    ang = cv2.getTrackbarPos("Rotate Angle", "Rotate Images")
    horizontal_count = cv2.getTrackbarPos("Horizontal Counting", "Rotate Images")

    now = datetime.datetime.now()
    hour = now.hour
    min = now.minute
    sec = now.second
    micrsec = now.microsecond
    ms = micrsec // 1000

    # CreateTxt(getgrad, hour, min, sec, ms)
    height_1 = cv2.getTrackbarPos("Height Start", "TrackBarsSize")
    height_2 = cv2.getTrackbarPos("Height End", "TrackBarsSize")
    weight_1 = cv2.getTrackbarPos("Weight Start", "TrackBarsSize")
    weight_2 = cv2.getTrackbarPos("Weight End", "TrackBarsSize")
    scale_percent = cv2.getTrackbarPos("Scale Percent", "TrackBarsSize")
    if scale_percent == 0:
        scale_percent = 1

    # Подсчёт значений по x, y
    x_left, y_down, x_right, y_up, gray = SelectMethod(img, r=r, g=g, b=b, scale=scale_percent, hsv=hsv_list, med=med)
    height_y, weight_x = gray.shape[:2]

    if horizontal_count == 0:
        th = GetRangeToHatch(height_y // 2)
        bth = GetRangeBetweenHatch(height_y // 2)
    else:
        th = GetRangeToHatch(weight_x // 2)
        bth = GetRangeBetweenHatch(weight_x // 2)

    # Штрихи
    # cv2.rectangle(gray, ((weight_2-weight_1)+100,round(th+height_y/2)),((weight_2-weight_1)-100,round(th+bth*8+height_y/2)),(0,255,0),4)
    # cv2.rectangle(gray, ((weight_2-weight_1)+100,round(height_y/2-th)),((weight_2-weight_1)-100,round(height_y/2-th-bth*8)),(0,255,0),4)

    # cv2.rectangle(gray, ((0),round(th+height_y/2)),((weight_x),round(th+bth*8+height_y/2)),(0,255,0),4)
    # cv2.rectangle(gray, ((0),round(height_y/2-th)),((weight_x),round(height_y/2-th-bth*8)),(0,255,0),4)
    # Центральная линия
    if horizontal_count == 0:
        # Штрихи
        cv2.rectangle(gray, ((0), round(th + height_y / 2)), ((weight_x), round(th + bth * 8 + height_y / 2)),
                      (0, 255, 0), 4)
        cv2.rectangle(gray, ((0), round(height_y / 2 - th)), ((weight_x), round(height_y / 2 - th - bth * 8)),
                      (0, 255, 0), 4)

        # Центральная линия
        # cv2.rectangle(imgContour, (0,((height_y)//2)), (1920,((height_y)//2)), (0,255,0), 6)
        cv2.rectangle(gray, (0, ((height_y) // 2)), (1920, ((height_y) // 2)), (0, 255, 0), 6)
    else:
        # Штрихи
        cv2.rectangle(gray, (round(th + weight_x / 2), 0), (round(th + bth * 8 + weight_x / 2), height_y), (0, 255, 0),
                      4)
        cv2.rectangle(gray, (round(weight_x / 2 - th), 0), (round(weight_x / 2 - th - bth * 8), height_y), (0, 255, 0),
                      4)

        # Центральная линия
        cv2.rectangle(gray, (((weight_x) // 2), 0), (((weight_x) // 2), 1920), (0, 255, 0), 6)
        cv2.rectangle(gray, (((weight_x) // 2), 0), (((weight_x) // 2), 1920), (0, 255, 0), 6)

        # Штрихи
        # cv2.rectangle(gray, (round(th+height_y/2),0),(round(th+bth*8+height_y/2),weight_x),(0,255,0),4)
        # cv2.rectangle(gray, (round(height_y/2-th),0),(round(height_y/2-th-bth*8),weight_x),(0,255,0),4)

        # Центральная линия
        # cv2.rectangle(imgContour, (((height_y)//2),0), (((height_y)//2),1920), (0,255,0), 6)
        # cv2.rectangle(gray, (((height_y)//2),0), (((height_y)//2),1920), (0,255,0), 6)

    # print(f"y[up] = {y_up}")
    # print(f"y[down] = {y_down}")
    y_ex = Extreme_Values(y_up, y_down, height_y / 2)
    x_ex = Extreme_Values(x_left, x_right, weight_x / 2)
    # print(f"y_ex = {y_ex}")

    # print(f"th = {th}")
    # print(f"bth = {bth}")
    if bth == 0:
        bth = 1
    if th == 0:
        th = 1

    maxgrad = countSec * 4
    if horizontal_count == 0:
        # print(f"GetGradus = {GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)}")
        if getgrad == "NONE":
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
        elif getgrad == ">" + str(maxgrad):
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = ">" + str(maxgrad)
        elif getgrad == "<-" + str(maxgrad):
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = "<-" + str(maxgrad)
        elif getgrad == "~=0":
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
        elif getgrad > 0:
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = ">" + str(maxgrad)
        elif getgrad <= 0:
            getgrad = GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = "<-" + str(maxgrad)
    else:
        # print(f"GetGradus = {GetGradus(th, bth, y_ex, weight_x // 2, horizontal_count)}")
        if getgrad == "NONE":
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
        elif getgrad == ">" + str(maxgrad):
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = ">" + str(maxgrad)
        elif getgrad == "<-" + str(maxgrad):
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = "<-" + str(maxgrad)
        elif getgrad == "~=0":
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
        elif getgrad > 0:
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = ">" + str(maxgrad)
        elif getgrad <= 0:
            getgrad = GetGradus(th, bth, x_ex, weight_x // 2, horizontal_count)
            if getgrad == "NONE":
                getgrad = "<-" + str(maxgrad)

    # Заполнение информационного окна
    winfo = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(winfo, f"Отклонение пузырька = {getgrad}''", (0, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_EX = {x_ex}px", (0, 200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"Center = {weight_x / 2}px", (0, 250), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_left = {x_left}px", (0, 300), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_right = {x_right}px", (0, 350), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"SR_arifm = {(x_left + x_right) / 2}px", (0, 400), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0),
                2)
    cv2.putText(winfo, f"bth = {bth}px", (0, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"count_sec = {get_second_method(x_left, y_down, x_right, y_up, horizontal_count, 0.314311216, weight_x, height_y)}''", (0, 500), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)

    # Отображение изображений
    # cv2.imshow("Video imgStackimgContour", imgStack)
    viewImage(gray, "gray", scale_percent)  ## 3
    cv2.imshow("Window", winfo)
    # cv2.imshow("Line", img_With_Line)
    # cv2.imshow("iC2", imgContour2)
    # cv2.imshow("Original", imgoriginal)

    zapis = False
    if zapis:
        out.write(img)

    h_min, h_max, s_min, s_max, v_min, v_max = 0, 0, 0, 0, 0, 0
    h2_min, h2_max, s2_min, s2_max, v2_min, v2_max = 0, 0, 0, 0, 0, 0
    FilterKernel, FilterKernel2 = 0, 0
    Median2 = 0

    with open("data.txt", "w") as file:
        file.write(str(ang) + "\n")

        file.write(str(h_min) + "\n")
        file.write(str(h_max) + "\n")
        file.write(str(s_min) + "\n")
        file.write(str(s_max) + "\n")
        file.write(str(v_min) + "\n")
        file.write(str(v_max) + "\n")

        file.write(str(height_1) + "\n")
        file.write(str(height_2) + "\n")
        file.write(str(weight_1) + "\n")
        file.write(str(weight_2) + "\n")
        file.write(str(scale_percent) + "\n")

        file.write(str(h2_min) + "\n")
        file.write(str(h2_max) + "\n")
        file.write(str(s2_min) + "\n")
        file.write(str(s2_max) + "\n")
        file.write(str(v2_min) + "\n")
        file.write(str(v2_max) + "\n")

        file.write(str(FilterKernel) + "\n")
        file.write(str(FilterKernel2) + "\n")
        file.write(str(Median2) + "\n")
        file.write(str(horizontal_count) + "\n")

        file.write(str(h_min_nm) + "\n")
        file.write(str(h_max_nm) + "\n")
        file.write(str(s_min_nm) + "\n")
        file.write(str(s_max_nm) + "\n")
        file.write(str(v_min_nm) + "\n")
        file.write(str(v_max_nm) + "\n")

        file.write(str(r) + "\n")
        file.write(str(g) + "\n")
        file.write(str(b) + "\n")
        file.write(str(med) + "\n")

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out.release()
        break