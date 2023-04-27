import cv2 as cv
from cv2 import CAP_PROP_FRAME_HEIGHT
from cv2 import CAP_PROP_FRAME_WIDTH
import threading
import numpy as np
import imutils


class Detector_class:
    ADthread = None
    Mark_dict = dict()
    _bx = -1  # _bx and _by are ball coords
    _by = -1
    run = True

    tick_count = 0

    def __init__(self) -> None:
        self.ADthread = threading.Thread(target=self.main, args=())
        self.ADthread.start()


    def stop(self):
        self.run = False
    

    def __getitem__(self, index: int) -> list:
        '''
        if index in self.Mark_dict:
            return self.Mark_dict[index]
        elif index == 0:
            return len(self.Mark_dict)
        else:
            return [-1, -1, 0]
        '''
        # index - НЕ ИД МАРКЕРА, А ТУПО НОМЕР ПАРЫ ПО ПОРЯДКУ. МЕТОД ВОЗВРАЩАЕТ ПАРУ (ИД, [ТРОЙКА])

        if index == 99:
            return len(self.Mark_dict)
        elif index == 77:
            return [self._bx, self._by]
        elif index >= len(self.Mark_dict):
            return [-1, -1, 0]
        else:
            return(list(self.Mark_dict.items())[index])
    

    def main(self):
        print("aruco detector __init__")
        # Загрузить предопределенный словарь aruco-маркеров
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)

        # Инициализировать параметры детектора, используя значения по умолчанию
        detector_parameters =  cv.aruco.DetectorParameters()
        ar_detector = cv.aruco.ArucoDetector(dictionary, detector_parameters)

        font = cv.FONT_HERSHEY_SIMPLEX
        font_color = (0, 255, 255)
        text_origin = 10, 20

        ball_color_lower = (98, 98, 78)
        ball_color_upper = (226, 255, 255)

        my_capture_picture_width = 1280
        my_capture_image_height = 720
        my_ballprocess_image_width = 600
        my_ballprocess_ratio = my_capture_picture_width/my_ballprocess_image_width

        cap = cv.VideoCapture()
        cap.open(cv.CAP_DSHOW)

        cap.set(CAP_PROP_FRAME_WIDTH, my_capture_picture_width) 
        cap.set(CAP_PROP_FRAME_HEIGHT, my_capture_image_height)

        if not cap.isOpened():
            print('Cannot open camera')
        else:
            
            do_your_job = True
            while do_your_job:
                self.tick_count += 1

                #time.sleep(1)
                # Capture frame-by-frame
                get, frame = cap.read()
                
                # if frame is read correctly get is True
                if not get:
                    print("Can't receive frame (stream end?). Exiting")
                    do_your_job = False
                else:
                    do_your_job = self.run
                    
                    # main image processing is here
                    
                    #FIRST FIND A BALL ONTO IMAGE
                    # ball_frame = imutils.resize(frame, width=my_ballprocess_image_width)

                    blurred_bframe = cv.GaussianBlur(frame, (11, 11), 0)
                    hsv = cv.cvtColor(blurred_bframe, cv.COLOR_BGR2HSV)
                    mask = cv.inRange(hsv, ball_color_lower, ball_color_upper)
                    mask = cv.erode(mask, None, iterations=2)
                    mask = cv.dilate(mask, None, iterations=2)
                    
                    # find contours in the mask and initialize the current
                    # (x, y) center of the ball
                    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)
                    center = None

                    # only proceed if at least one contour was found
                    if len(cnts) > 0:
		                # find the largest contour in the mask, then use
		                # it to compute the minimum enclosing circle and
		                # centroid
                        c = max(cnts, key=cv.contourArea)
                        ((x, y), radius) = cv.minEnclosingCircle(c)
                        M = cv.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		                
                        # only proceed if the radius meets a minimum size
                        if radius > 10:
                            # draw the circle and centroid on the frame,
                            # then update the list of tracked points
                            cv.circle(frame, 
                                        (int(x), int(y)), int(radius),
				                        (0, 255, 255), 2)
                            self._bx = int(x)
                            self._by = int(y)
                            # cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    else:
                        self._bx = -1
                        self._by = -1
                    
                    # ###
                    # now let's process markers
                    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    markerCoord, markerValue, rejectedCandidates = ar_detector.detectMarkers(gray)  # corners, ids, rejected xxx
                    # markerCoord is OutputArrayOfArrays
                    if markerCoord:
                        marks = zip(markerValue, markerCoord)  # marks is zip of tuples
                        for mark in marks:
                            # mark is tuple (Value, coords - ArrayOfArrays)
                            
                            # print('type of mark[1] is', type(mark[1]), 'shape', mark[1].shape)
                            # mark[1] is ndarray shape is (1, 4, 2) - coords of four marker corners

                            # print('type of mark[0] is', type(mark[0]), 'shape', mark[0].shape)
                            # mark[0] is ndarray shape is (1,) - means one-element-list - MARKER VALUE

                            a = mark[1].astype(np.int32)
                            coord = a[0]   # coord is 2-dimensional array, each element is [x, y]
                            centre = (coord[0][0]+coord[2][0])//2, (coord[0][1]+coord[2][1])//2
                            angle = np.arctan((coord[2][0]-coord[0][0])/(coord[2][1]-coord[0][1]))
                            
                            self.Mark_dict[mark[0][0]] = [centre[0], centre[1], angle]
                            frame = cv.polylines(frame, a, True, [0, 255, 0], 5)
                            cv.putText(frame, f'{mark[0]}', centre, font, 1,(0,100,255),2,cv.LINE_AA)

                    
                    cv.putText(frame, "press 'q' to close this picture", text_origin, font, 0.5, font_color)
                    cv.imshow('frame', frame)

                    # cv.putText(mask, "press 'q' to close this picture", text_origin, font, 0.5, font_color)
                    # cv.imshow('mask', mask)

                    if cv.waitKey(1) == ord('q'):
                        do_your_job = False


            # When everything done, release the capture
            self.run = False
            cap.release()
            cv.destroyAllWindows()