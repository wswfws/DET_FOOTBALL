import cv2 as cv
import numpy as np
# Загрузить предопределенный словарь
dictionary=cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
# Сгенерировать маркер
num = int(input("input num of marker"))
markerImage = cv.aruco.generateImageMarker(dictionary, num, 200)
cv.imwrite(f"marker{num}.png", markerImage)
