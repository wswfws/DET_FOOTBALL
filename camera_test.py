import cv2 as cv
import time

# cap = cv.VideoCapture(0)

cap = cv.VideoCapture()
cap.open(cv.CAP_DSHOW)

time.sleep(5)

if not cap.isOpened():
    print('Cannot open camera')
else:
    print('successfully open camera')
