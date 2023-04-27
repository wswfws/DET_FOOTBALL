import cv2 as cv
from cv2 import CAP_PROP_FRAME_HEIGHT
from cv2 import CAP_PROP_FRAME_WIDTH
from cv2 import CAP_PROP_FPS
import numpy as np
import time
import threading

class Detect:
    det = None
    Mark = dict()
    run = True

    def __init__(self) -> None:
        self.det = threading.Thread(target=self.main, args=())
        self.det.start()

    def main(self):
        print("__init__")
        # Загрузить предопределенный словарь
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)

        # Инициализировать параметры детектора, используя значения по умолчанию
        parameters =  cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)
        font = cv.FONT_HERSHEY_SIMPLEX

        # cap = cv.VideoCapture(0)
        # cap = cv.VideoCapture(2)
        cap = cv.VideoCapture()
        cap.open(1 + cv.CAP_DSHOW)
        # cap.open(cv.CAP_DSHOW)
        cap.set(CAP_PROP_FRAME_WIDTH , 1280); 
        cap.set(CAP_PROP_FRAME_HEIGHT , 720); 
        # cap.set(CAP_PROP_FRAME_WIDTH , 640); 
        # cap.set(CAP_PROP_FRAME_HEIGHT , 480); 
        # cap.set(CAP_PROP_FPS, 25) 
        # cap.set(CAP_PROP_FRAME_WIDTH , 1920); 
        # cap.set(CAP_PROP_FRAME_HEIGHT , 1080); 
        # 1920x1080

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while self.run:
            #time.sleep(1)
            # Capture frame-by-frame
            get, frame = cap.read()
            # if frame is read correctly ret is True
            if not get:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here
            
            '''
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            markerCord, markerValue, rejectedCandidates = detector.detectMarkers(gray)
            if markerCord:
                marks = zip(markerValue, markerCord)
                for mark in marks:
                    a = mark[1].astype(np.int32)
                    cord = a[0]
                    centre = (cord[0][0]+cord[2][0])//2, (cord[0][1]+cord[2][1])//2
                    angle = np.arctan((cord[2][0]-cord[0][0])/(cord[2][1]-cord[0][1]))
                    
                    self.Mark[mark[0][0]] = [centre, angle]
                    frame = cv.polylines(frame, a, True, [0, 255, 0], 5)
                    cv.putText(frame, f'{mark[0]}', centre, font, 1,(0,100,255),2,cv.LINE_AA)
            '''
            # Display the resulting frame
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()
            # Обнаружение маркеров на изображении

    def get_Mark(self, val):
        return self.Mark.get(val, None)
    
    def stop(self):
        self.run = False