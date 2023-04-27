import threading
import time
import datetime
# from tkinter import *
# from tkinter import ttk

from ev3msg import EV3
# from detect import Detect
from arucodetector import Detector_class


def check_cord(cord):
    if cord is None:
        return False
    if cord[0]<=0 or cord[1]<=0:
        return False
    else:
        return True


def add_to_bricks(brick_id):
    a = brick_id.find('#')
    
    if a != -1:
        s = brick_id[:a].strip()
    else:
        s = brick_id.strip()
    
    if len(s) != 0:
        # connect to brick
        bricks.append(s)


def read_bricks():
    f = open('config.ini')
    for s in f.readlines():
        add_to_bricks(s)
    f.close()


def connect_to_bricks():
    for i in range(len(bricks)):
        print('connecting', bricks[i], '...')
        ev3 = EV3(bricks[i])
        bricks[i] = ev3


def message_handler():
    msgs = messeges
    for msg in msgs:
        for brick in bricks:
            brick.send(msg[0], msg[1])


bricks = []

Marks = dict()
messeges = list()   #  [[title:str, value:{str, int, float}]]

read_bricks()
print('bricks are', bricks)
connect_to_bricks()
# time.sleep(5)

print('create aruco detector')
detectorobject = Detector_class()

print('testing detector for 5 sec...')
time.sleep(5)

if not detectorobject.run:
    print('detector not opened')
else:
    print('success detector init with', detectorobject.tick_count, 'ticks')
    
    # do main program here
    
    # run = True
    while detectorobject.run:
        # run = detectorobject.run
        
        if detectorobject[99] == 0:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: nothing to send")
        else:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: send to all bricks:", end=' ')
            for i in range(detectorobject[99]):
                print(detectorobject[i], end='  ')
            
            print(detectorobject[77])

            for brick in bricks:
                # print(f"send to brick {i}: {detectorobject[i]}", end = ' | ')
                # messeges.append([f"x{i}", detectorobject[i]])
                for i in range(detectorobject[99]):
                    brick.send_message(f'x{detectorobject[i][0]}', detectorobject[i][1][0].item())  # x-coordinate 
                    time.sleep(0.1)
                    brick.send_message(f'y{detectorobject[i][0]}', detectorobject[i][1][1].item())  # y-coordinate
                    time.sleep(0.1)
                    brick.send_message(f'a{detectorobject[i][0]}', detectorobject[i][1][2].item())  # angle
                    time.sleep(0.1)
                    
                ball_coords = detectorobject[77]
                brick.send_message('bx', ball_coords[0])
                time.sleep(0.1)
                brick.send_message('by', ball_coords[1])
                time.sleep(0.1)

        #print(f"time = {datetime.datetime.now().time()}")

        # message_handler()
        
        time.sleep(1)

    # detectorobject.stop()
    # print('end with tick count', detectorobject.tick_count)
    