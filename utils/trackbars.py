import cv2

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

# Кропы (ну ты понял)
height_1T = 120
height_2T = 1016
weight_1T = 440
weight_2T = 540

scale_percentT = 50
horizontal_countT = 0

w_2_leftT = 10
w_1_rightT = 200

# Настройки которые ты крутил обычно (ну ты понял, да?)
h_minT, h_maxT, s_minT, s_maxT, v_minT, v_maxT = 0, 255, 0, 96, 130, 255
h2_minT, h2_maxT, s2_minT, s2_maxT, v2_minT, v2_maxT = 0, 255, 0, 96, 130, 255
h_min_nmT, h_max_nmT, s_min_nmT, s_max_nmT, v_min_nmT, v_max_nmT = 73, 255, 75, 255, 0, 255
rT, gT, bT, mT = 215, 240, 241, 0
angT = 0
FilterKernelT = 1
FilterKernelT2 = 1
MedianT2 = 1

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

def draw_trackbars():
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


    ang = cv2.getTrackbarPos("Rotate Angle", "Rotate Images")
    horizontal_count = cv2.getTrackbarPos("Horizontal Counting", "Rotate Images")

    height_1 = cv2.getTrackbarPos("Height Start", "TrackBarsSize")
    height_2 = cv2.getTrackbarPos("Height End", "TrackBarsSize")
    weight_1 = cv2.getTrackbarPos("Weight Start", "TrackBarsSize")
    weight_2 = cv2.getTrackbarPos("Weight End", "TrackBarsSize")
    scale_percent = cv2.getTrackbarPos("Scale Percent", "TrackBarsSize")

    return r, g, b, med, [h_min_nm, h_max_nm, s_min_nm, s_max_nm, v_min_nm, v_max_nm], ang, horizontal_count