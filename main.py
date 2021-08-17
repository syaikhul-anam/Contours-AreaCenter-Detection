#import library
import cv2
import numpy as np
import imutils


def nothing(x):
    pass

#pengambilan video melalui kamera
cap = cv2.VideoCapture(0)

#pembuatan jendela trackbars
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

#resolusi kamera yang dipakai (prodId, value)
cap.set(4, 640)
cap.set(3, 480)

while True:
    _, frame = cap.read()
    #tranformasi warna RGB to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    #inisialisasi untuk batas terendah dan tertinggi
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    #mask untuk melihat hasil transformasi ke hsv
    mask = cv2.inRange(hsv, lower_color, upper_color)
    #result untuk melihat hasil warna
    result = cv2.bitwise_and(frame, frame, mask=mask)
    #deteksi area
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:

            cv2.drawContours(frame, [c], -1, (0, 255, 200), 3)

            M = cv2.moments(c)
            #koordinat untuk titik tengah
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Centre", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 1)

            print("area is ...", area)
            print("centroid is at..", cx, cy)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


