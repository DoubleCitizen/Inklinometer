import cv2
import numpy as np
import math
import datetime
import imutils
import os

from PIL import Image, ImageEnhance

# path = "Resources/IMG_21.mov"
# path = "Resources/normal/IMG_6050.mov"

# path = "Resources/Fresh/IMG_6306.mov"
path = "output_video3.avi"
#path = 0
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

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("H Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("H Max", "TrackBars", 0, 255, empty)
cv2.createTrackbar("S Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("S Max", "TrackBars", 0, 255, empty)
cv2.createTrackbar("V Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("V Max", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Filter Kernel", "TrackBars", 1, 10, empty)

cv2.namedWindow("HSV Post Proccesing")
cv2.resizeWindow("HSV Post Proccesing", 640, 300)
cv2.createTrackbar("H Min", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("H Max", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("S Min", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("S Max", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("V Min", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("V Max", "HSV Post Proccesing", 0, 255, empty)
cv2.createTrackbar("Filter Kernel", "HSV Post Proccesing", 1, 10, empty)
cv2.createTrackbar("Median", "HSV Post Proccesing", 1, 10, empty)

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

def viewImage(name, str):
    cv2.imshow(str, name)

def getCont(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for id, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 200 and area < 5800:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return x, y, x + w, y + h

def SelectMethod(image, r=215, g=236, b=241, scale=100, hsv=[0, 255, 56, 255, 0, 255]):

    image = cv2.resize(image, Get_ResizePicture(image, scale))

    lower = np.array((hsv[0], hsv[2], hsv[4]), np.uint8)
    upper = np.array((hsv[1], hsv[3], hsv[5]), np.uint8)

    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    viewImage(hsv_img, "hsv_img")  ## 1
    #lower = np.array([188, 199, 219])
    #upper = np.array([208, 219, 241])
    curr_mask = cv2.inRange(hsv_img, lower, upper)
    hsv_img[curr_mask > 0] = ([208, 255, 200])
    viewImage(hsv_img, "hsv_img")  ## 2

    # Фильтрация
    ## Преобразование HSV-изображения к оттенкам серого для дальнейшего
    ## оконтуривания
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

    ret, threshold = cv2.threshold(gray, r, g, b)
    viewImage(threshold, "threshold")  ## 4
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        x1, y1, x2, y2 = getCont(threshold)
        cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
    except:
        x1, y1, x2, y2 = 0, 0, 0, 0
    viewImage(gray, "gray")  ## 3

    cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    viewImage(image, "image")  ## 5
    return x1, y1, x2, y2

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
    print(f"otvet = (h - y) / Rel_between_hatch_to_end")
    print(f"{otvet} = ({h} - {y}) / {Rel_between_hatch_to_end}")
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
    print("=======")
    print(f"y_ex(y) = {y}")
    y -= center
    print(f"y - center = {y}")
    print(f"centerDiap = {centerDiap}")
    print(f"diap1 = {diap1}")
    print(f"diap2 = {diap2}")
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


def getContours(img, img2):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x_arr = []
    y_arr = []
    h_arr = []
    w_arr = []
    for id, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 200 and area < 5800:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            x_arr.append(x)
            y_arr.append(y)
            try:
                av_y = round(Aver_Arif(y_arr))
                dev_y = Deviation(y_arr, av_y)
                skp_y = round(SKP(dev_y))

                av_x = round(Aver_Arif(x_arr))
                dev_x = Deviation(x_arr, av_x)
                skp_x = round(SKP(dev_x))
            except:
                continue

            h_arr.append(h)
            av_h = round(Aver_Arif(h_arr))
            dev_h = Deviation(h_arr, av_h)
            skp_h = round(SKP(dev_h))

            w_arr.append(w)
            av_w = round(Aver_Arif(w_arr))
            dev_w = Deviation(w_arr, av_w)
            skp_w = round(SKP(dev_w))

            # Вертикалка
            y_arr_new = exception_anomalies(skp_y, SKO, y_arr)
            y_aver_new = round(Aver_Arif(y_arr_new))

            h_arr_new = exception_anomalies(skp_h, SKO, h_arr)
            h_aver_new = round(Aver_Arif(h_arr_new))
            # Вертикалка

            # Горизонталка
            x_arr_new = exception_anomalies(skp_x, SKO, x_arr)
            x_aver_new = round(Aver_Arif(x_arr_new))

            w_arr_new = exception_anomalies(skp_w, SKO, w_arr)
            w_aver_new = round(Aver_Arif(w_arr_new))
            # Горизонталка

            global y_up, y_down, x_left, x_right
            y_up = y_aver_new
            y_down = y_aver_new + h_aver_new
            x_left = x_aver_new
            x_right = x_aver_new + w_aver_new

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return y_down, y_up, x_left, x_right


def getContours2(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    y_arr = []
    h_arr = []
    area_arr = []
    area_max = 0
    id_max = 0

    x_down_max = 0
    x_up_max = 0
    y_down_max = 0
    y_up_max = 0

    maxarea = mwei * mhei - 10000

    for id, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 0 and area < maxarea:

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            area_arr.append(area)
            x, y, w, h = cv2.boundingRect(approx)

            if area_max < area:
                area_max = area
                id_max = id

                x_down_max = x
                y_down_max = y

                x_up_max = x + w
                y_up_max = y + h

            cv2.rectangle(imgContour2, (x_down_max, y_down_max), (x_up_max, y_up_max), (0, 255, 0), 10)
            # cv2.rectangle(img2, (x_down_max,y_down_max), (x_up_max,y_up_max), (0,255,0), 2)

    return x_down_max, x_up_max, y_down_max, y_up_max


# with open("data.txt", "w") as file:
#        file.write(ang + " ")

#        file.write(h_min + " ")
#        file.write(h_max + " ")
#        file.write(s_min + " ")
#        file.write(s_max + " ")
#        file.write(v_min + " ")
#        file.write(v_max + " ")

#        file.write(height_1 + " ")
#        file.write(height_2 + " ")
#        file.write(weight_1 + " ")
#        file.write(weight_2 + " ")


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
except:
    print("NULL Data.txt")
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

w_2_leftT = 10
w_1_rightT = 200

out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (640, 480))

ang = cv2.setTrackbarPos("Rotate Angle", "Rotate Images", angT)
horizontal_count = cv2.setTrackbarPos("Horizontal Counting", "Rotate Images", horizontal_countT)
h_min = cv2.setTrackbarPos("H Min", "TrackBars", h_minT)
h_max = cv2.setTrackbarPos("H Max", "TrackBars", h_maxT)
s_min = cv2.setTrackbarPos("S Min", "TrackBars", s_minT)
s_max = cv2.setTrackbarPos("S Max", "TrackBars", s_maxT)
v_min = cv2.setTrackbarPos("V Min", "TrackBars", v_minT)
v_max = cv2.setTrackbarPos("V Max", "TrackBars", v_maxT)
FilterKernel = cv2.setTrackbarPos("Filter Kernel", "TrackBars", FilterKernelT)

h2_min = cv2.setTrackbarPos("H Min", "HSV Post Proccesing", h2_minT)
h2_max = cv2.setTrackbarPos("H Max", "HSV Post Proccesing", h2_maxT)
s2_min = cv2.setTrackbarPos("S Min", "HSV Post Proccesing", s2_minT)
s2_max = cv2.setTrackbarPos("S Max", "HSV Post Proccesing", s2_maxT)
v2_min = cv2.setTrackbarPos("V Min", "HSV Post Proccesing", v2_minT)
v2_max = cv2.setTrackbarPos("V Max", "HSV Post Proccesing", v2_maxT)
FilterKernel2 = cv2.setTrackbarPos("Filter Kernel", "HSV Post Proccesing", FilterKernelT2)
Median2 = cv2.setTrackbarPos("Median", "HSV Post Proccesing", MedianT2)

height_1 = cv2.setTrackbarPos("Height Start", "TrackBarsSize", height_1T)
height_2 = cv2.setTrackbarPos("Height End", "TrackBarsSize", height_2T)
weight_1 = cv2.setTrackbarPos("Weight Start", "TrackBarsSize", weight_1T)
weight_2 = cv2.setTrackbarPos("Weight End", "TrackBarsSize", weight_2T)

height_1 = cv2.setTrackbarPos("Height Start", "TrackBarsSize", height_1T)
height_2 = cv2.setTrackbarPos("Height End", "TrackBarsSize", height_2T)
weight_1 = cv2.setTrackbarPos("Weight Start", "TrackBarsSize", weight_1T)
weight_2 = cv2.setTrackbarPos("Weight End", "TrackBarsSize", weight_2T)

scale_percent = cv2.setTrackbarPos("Scale Percent", "TrackBarsSize", scale_percentT)

# cv2.namedWindow("Rectangles")
# cv2.resizeWindow("Rectangles", 600,200)
# cv2.createTrackbar("Left Rect", "Rectangles", 0, 400,empty)
# cv2.createTrackbar("Right Rect", "Rectangles", 0, 400,empty)

w_2_left = cv2.setTrackbarPos("Left Rect", "Rectangles", w_2_leftT)
w_1_right = cv2.setTrackbarPos("Right Rect", "Rectangles", w_1_rightT)

while (cap.isOpened()):

    h_min = cv2.getTrackbarPos("H Min", "TrackBars")
    h_max = cv2.getTrackbarPos("H Max", "TrackBars")
    s_min = cv2.getTrackbarPos("S Min", "TrackBars")
    s_max = cv2.getTrackbarPos("S Max", "TrackBars")
    v_min = cv2.getTrackbarPos("V Min", "TrackBars")
    v_max = cv2.getTrackbarPos("V Max", "TrackBars")
    FilterKernel = cv2.getTrackbarPos("Filter Kernel", "TrackBars")
    horizontal_count = cv2.getTrackbarPos("Horizontal Counting", "Rotate Images")

    h2_min = cv2.getTrackbarPos("H Min", "HSV Post Proccesing")
    h2_max = cv2.getTrackbarPos("H Max", "HSV Post Proccesing")
    s2_min = cv2.getTrackbarPos("S Min", "HSV Post Proccesing")
    s2_max = cv2.getTrackbarPos("S Max", "HSV Post Proccesing")
    v2_min = cv2.getTrackbarPos("V Min", "HSV Post Proccesing")
    v2_max = cv2.getTrackbarPos("V Max", "HSV Post Proccesing")
    FilterKernel2 = cv2.getTrackbarPos("Filter Kernel", "HSV Post Proccesing")
    Median2 = cv2.getTrackbarPos("Median", "HSV Post Proccesing")

    lower = np.array((h_min, s_min, v_min), np.uint8)
    upper = np.array((h_max, s_max, v_max), np.uint8)

    lower2 = np.array((h2_min, s2_min, v2_min), np.uint8)
    upper2 = np.array((h2_max, s2_max, v2_max), np.uint8)

    try:
        success, img = cap.read()
    except:
        continue

    if success == False:
        cap = cv2.VideoCapture(path)
        success, img = cap.read()

    ang = cv2.getTrackbarPos("Rotate Angle", "Rotate Images")
    img = imutils.rotate(img, angle=ang)

    mwei, mhei = img.shape[:2]

    w_1_left = 0
    w_2_right = mwei

    w_2_left = cv2.getTrackbarPos("Left Rect", "Rectangles")
    w_1_right = cv2.getTrackbarPos("Right Rect", "Rectangles")

    height_1 = cv2.getTrackbarPos("Height Start", "TrackBarsSize")
    height_2 = cv2.getTrackbarPos("Height End", "TrackBarsSize")
    weight_1 = cv2.getTrackbarPos("Weight Start", "TrackBarsSize")
    weight_2 = cv2.getTrackbarPos("Weight End", "TrackBarsSize")
    scale_percent = cv2.getTrackbarPos("Scale Percent", "TrackBarsSize")
    if scale_percent == 0:
        scale_percent = 1

    imgCropped = img[height_1:height_2, weight_1:weight_2]

    imgCropped2 = img[height_1:height_2, weight_1:weight_2]
    img_With_Line = img[height_1:height_2, weight_1:weight_2]

    img = img[height_1:height_2, weight_1:weight_2]

    # imgCanny = cv2.Canny(imgCropped, 35, 35)

    # prepare the 5x5 shaped filter
    kernel = np.array([[1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1]])

    if FilterKernel < 1:
        FilterKernel = 1
    kernel = np.full((FilterKernel, FilterKernel), 1)

    kernel = kernel / sum(kernel)
    # img_With_Line = imgCanny

    # filter the source image
    img_With_Line = cv2.filter2D(imgCropped, -1, kernel)

    imgoriginal = img

    hsv = cv2.cvtColor(img_With_Line, cv2.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    thresh = cv2.inRange(hsv, lower, upper)  # применяем цветовой фильтр

    imgContour2 = thresh.copy()

    # imgoriginal = imutils.rotate(imgoriginal, angle=ang)
    # gray = imutils.rotate(gray, angle=ang)
    # imgContour = imutils.rotate(imgContour, angle=ang)

    # Белые прямоугольники слева и справа
    # cv2.rectangle(imgContour, (w_1_left,0),(w_2_left,mhei),(255,255,255),cv2.FILLED)
    # cv2.rectangle(imgContour, (w_1_right,0),(w_2_right,mhei),(255,255,255),cv2.FILLED)
    # Белые прямоугольники
    # cv2.rectangle(imgContour, (0,round(height_y/2+th+bth*8)+30),(1920,1080),(255,255,255),cv2.FILLED)
    # cv2.rectangle(imgContour, (0,0),(1920,round(height_y/2-th-bth*8)-30),(255,255,255),cv2.FILLED)

    now = datetime.datetime.now()
    hour = now.hour
    min = now.minute
    sec = now.second
    micrsec = now.microsecond
    ms = micrsec // 1000

    # CreateTxt(getgrad, hour, min, sec, ms)

    # Рисовалка зелёный линии

    X1, X2, Y1, Y2 = getContours2(imgContour2)
    if X2 <= X1 + 10 or Y2 <= Y1 + 10:
        X1, X2, Y1, Y2 = 0, mwei, 0, mhei
    imgCropped2 = img[Y1:Y2, X1:X2]
    cv2.rectangle(img_With_Line, (X1, Y1), (X2, Y2), (0, 255, 0), 10)

    # Масштабирование

    imgCropped2 = cv2.resize(imgCropped2, Get_ResizePicture(imgCropped2, scale_percent))
    img_With_Line = cv2.resize(img_With_Line, Get_ResizePicture(img_With_Line, scale_percent))

    imgoriginal = cv2.resize(imgoriginal, Get_ResizePicture(imgoriginal, scale_percent))
    imgContour2 = cv2.resize(imgContour2, Get_ResizePicture(imgContour2, scale_percent))
    # imgCanny = cv2.resize(imgCanny, Get_ResizePicture(imgCanny, scale_percent))

    # imgStack2 = np.concatenate((imgCropped2, img_With_Line), axis=1)

    # Пост Обработка ++++++++++++++++++++++++++++++++++++++++++++

    # Фильтрация изображения

    if FilterKernel2 > 1:
        kernel = np.full((FilterKernel2, FilterKernel2), 1)

        kernel = kernel / sum(kernel)

        # filter the source image
        imgCropped2 = cv2.filter2D(imgCropped2, -1, kernel)

    Median2NeChet = Median2
    if Median2 > 1:
        if Median2 % 2 == 0:
            Median2NeChet += 1
        imgCropped2 = cv2.medianBlur(imgCropped2, Median2NeChet)

    # Фильтрация изображения

    gray_low = np.array([193, 206, 231])
    gray_high = np.array([206, 219, 241])

    # imgCropped2 = np.uint8([[[196, 207, 237 ]]]) # меняем цветовую модель с BGR на HSV
    hsv2 = cv2.cvtColor(imgCropped2, cv2.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    curr_mask = cv2.inRange(hsv2, gray_low, gray_high)
    hsv2[curr_mask > 0] = ([206, 219, 200])
    thresh2 = cv2.inRange(hsv2, lower2, upper2)  # применяем цветовой фильтр

    imgContour = thresh2.copy()
    gray = cv2.cvtColor(imgCropped2, cv2.COLOR_BGR2GRAY)

    # enhancer = ImageEnhance.Contrast(imgContour)
    # enhancer2 = ImageEnhance.Contrast(gray)

    # imgContour = enhancer.enhance(brightness)
    # gray = enhancer2.enhance(brightness)

    y_down, y_up, x_left, x_right = getContours(imgContour, gray)
    if y_down < 0:
        print("ERROR")

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
        cv2.rectangle(imgContour, (0, ((height_y) // 2)), (1920, ((height_y) // 2)), (0, 255, 0), 6)
        cv2.rectangle(gray, (0, ((height_y) // 2)), (1920, ((height_y) // 2)), (0, 255, 0), 6)
    else:
        # Штрихи
        cv2.rectangle(gray, (round(th + weight_x / 2), 0), (round(th + bth * 8 + weight_x / 2), height_y), (0, 255, 0),
                      4)
        cv2.rectangle(gray, (round(weight_x / 2 - th), 0), (round(weight_x / 2 - th - bth * 8), height_y), (0, 255, 0),
                      4)

        # Центральная линия
        cv2.rectangle(imgContour, (((weight_x) // 2), 0), (((weight_x) // 2), 1920), (0, 255, 0), 6)
        cv2.rectangle(gray, (((weight_x) // 2), 0), (((weight_x) // 2), 1920), (0, 255, 0), 6)

        # Штрихи
        # cv2.rectangle(gray, (round(th+height_y/2),0),(round(th+bth*8+height_y/2),weight_x),(0,255,0),4)
        # cv2.rectangle(gray, (round(height_y/2-th),0),(round(height_y/2-th-bth*8),weight_x),(0,255,0),4)

        # Центральная линия
        # cv2.rectangle(imgContour, (((height_y)//2),0), (((height_y)//2),1920), (0,255,0), 6)
        # cv2.rectangle(gray, (((height_y)//2),0), (((height_y)//2),1920), (0,255,0), 6)

    print(f"y[up] = {y_up}")
    print(f"y[down] = {y_down}")
    y_ex = Extreme_Values(y_up, y_down, height_y / 2)
    x_ex = Extreme_Values(x_left, x_right, weight_x / 2)
    print(f"y_ex = {y_ex}")

    print(f"th = {th}")
    print(f"bth = {bth}")
    maxgrad = countSec * 4
    if horizontal_count == 0:
        print(f"GetGradus = {GetGradus(th, bth, y_ex, height_y // 2, horizontal_count)}")
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
        print(f"GetGradus = {GetGradus(th, bth, y_ex, weight_x // 2, horizontal_count)}")
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

    imgStack = np.concatenate((gray, imgContour), axis=1)

    # Пост Обработка ++++++++++++++++++++++++++++++++++++++++++++

    # Заполнение информационного окна
    winfo = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(winfo, f"Отклонение пузырька = {getgrad}''", (0, 200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_EX = {x_ex}''", (0, 250), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"Center = {weight_x / 2}''", (0, 300), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_left = {x_left}''", (0, 350), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"X_right = {x_right}''", (0, 400), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
    cv2.putText(winfo, f"SR_arifm = {(x_left + x_right) / 2}''", (0, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0),
                2)

    # cv2.imshow("Video imgStackimgContour", imgContour)
    # cv2.imshow("Video imgStackgray", gray)
    x1, y1, x2, y2 = SelectMethod(img, r=215, g=236, b=241, scale=scale_percent)
    cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Video imgStackimgContour", imgStack)

    # cv2.imshow("Original", imgoriginal)
    cv2.imshow("Window", winfo)
    # cv2.imshow("crop", imgCropped2)
    cv2.imshow("Line", img_With_Line)
    cv2.imshow("iC2", imgContour2)
    cv2.imshow("Original", imgoriginal)

    zapis = False
    if zapis:
        out.write(img)

    ## Кропы (ну ты понял)
    # height_1T = 120
    # height_2T = 1016
    # weight_1T = 440
    # weight_2T = 540
    ##Настройки которые ты крутил обычно (ну ты понял, да?)
    # h_minT, h_maxT, s_minT, s_maxT, v_minT, v_maxT = 0, 255, 0, 96, 130, 255
    # angT = 0

    # ang = cv2.setTrackbarPos("H Min", "TrackBars", angT)

    # h_min = cv2.setTrackbarPos("H Min", "TrackBars", h_minT)
    # h_max = cv2.setTrackbarPos("H Max", "TrackBars", h_maxT)
    # s_min = cv2.setTrackbarPos("S Min", "TrackBars", s_minT)
    # s_max = cv2.setTrackbarPos("S Max", "TrackBars", s_maxT)
    # v_min = cv2.setTrackbarPos("V Min", "TrackBars", v_minT)
    # v_max = cv2.setTrackbarPos("V Max", "TrackBars", v_maxT)

    # height_1 = cv2.setTrackbarPos("Height Start", "TrackBarsSize", height_1T)
    # height_2 = cv2.setTrackbarPos("Height End", "TrackBarsSize", height_2T)
    # weight_1 = cv2.setTrackbarPos("Weight Start", "TrackBarsSize", weight_1T)
    # weight_2 = cv2.setTrackbarPos("Weight End", "TrackBarsSize", weight_2T)

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

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out.release()
        break