# camKapture is an open source application that allows users to access their webcam device and take pictures or create videos.
import cv2
import math
import os
from datetime import datetime
import numpy as np

img_directory = os.path.expanduser('~')+r'/Pictures/camKapture/'
vid_directory = os.path.expanduser('~')+r'/Videos/camKapture/'

if not os.path.exists(img_directory):
    os.mkdir(img_directory)

if not os.path.exists(vid_directory):
    os.mkdir(vid_directory)

cap= cv2.VideoCapture(0)
cap.set(3,854)
cap.set(4,480)

def white_screen():
    frame=np.zeros([100,100,3],dtype=np.uint8)
    frame.fill(255)
    cv2.imshow('camKapture',frame)
    cv2.waitKey(100)

def count(n):
    coordinates=(400,250)
    font=cv2.FONT_HERSHEY_SIMPLEX
    fontScale=4
    color=(255,255,255)
    thickness=5
    j=(n+1)*10-1
    while True:
        success, frame1 = cap.read()
        success, frame2 = cap.read()
        cv2.imshow('camKapture', frame1)
        if j>=10:
            text=str(math.floor(j/10)) 
            cv2.putText(frame2,text,coordinates,font,fontScale,(0,0,0),thickness+2,cv2.LINE_AA)
            cv2.putText(frame2,text,coordinates,font,fontScale,color,thickness,cv2.LINE_AA)
            cv2.imshow('camKapture', frame2)
            cv2.waitKeyEx(100)
            j=j-1
        else:
            cv2.imshow('camKapture', frame1)
            cv2.imwrite(os.path.join(img_directory , str(datetime.now())+'.jpg'),frame1)
            white_screen()
            print('Image saved to '+os.path.join(img_directory , str(datetime.now())+'.jpg'))
            return

def burst():
    j=10
    while True :
        success, frame = cap.read()
        pressedKey = cv2.waitKeyEx(1) & 0xFF
        cv2.imshow('camKapture', frame)
        if j==0:
            cv2.imwrite(os.path.join(img_directory , str(datetime.now())+'.jpg'),frame)
            white_screen()
            print('Image saved to '+os.path.join(img_directory , str(datetime.now())+'.jpg'))
            j=10
        j=j-1
        if pressedKey == 8:
            print('Burst mode has ended')
            break
        elif pressedKey == 27:
            exit()
    return

def video():
    text='Recording...'
    coordinates=(0,20)
    font=cv2.FONT_HERSHEY_SIMPLEX
    fontScale=0.6
    color=(0,0,255)
    thickness=1

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    result = cv2.VideoWriter(os.path.join(vid_directory , str(datetime.now())+'.avi'),fourcc,10, size)
    unpaused=True

    while True:
        success, frame = cap.read()
        pressedKey = cv2.waitKeyEx(1) & 0xFF
        if success == True: 
            if(unpaused):
                result.write(frame)
            frame=cv2.putText(frame,text,coordinates,font,fontScale,(0,0,0),thickness+2,cv2.LINE_AA)
            frame=cv2.putText(frame,text,coordinates,font,fontScale,color,thickness,cv2.LINE_AA)
            cv2.imshow('camKapture', frame)

            if pressedKey == 8: # backspace to home
                result.release()
                print("Video saved to "+os.path.join(vid_directory , str(datetime.now())+'.avi'))
                return
            elif pressedKey == 27: # Esc to quit
                cap.release()
                result.release()
                cv2.destroyAllWindows()
                print("Video saved to "+os.path.join(vid_directory , str(datetime.now())+'.avi'))
                exit()
            elif pressedKey == 32:
                if unpaused:
                    coordinates=(300,250)
                    fontScale=2
                    color=(255,255,255)
                    thickness=3
                    text='paused'
                    unpaused=False
                else:
                    text='Recording...'
                    coordinates=(0,20)
                    fontScale=0.6
                    color=(0,0,255)
                    thickness=1
                    unpaused=True
        else:
            break

while True:
    success, frame = cap.read()
    
    cv2.namedWindow('camKapture', flags=cv2.WINDOW_GUI_NORMAL)
    cv2.imshow('camKapture',frame)  
    cv2.resizeWindow('camKapture', 854, 480)

    pressedKey = cv2.waitKeyEx(1) & 0xFF

    if pressedKey == ord("s"): # press s to save a frame
        cv2.imwrite(os.path.join(img_directory , str(datetime.now())+'.jpg'),frame)
        white_screen()
        print('Image saved to '+os.path.join(img_directory , str(datetime.now())+'.jpg'))
    elif pressedKey == ord("v"): # press v to enter video mode
        cv2.setWindowTitle('camKapture', 'camKapture - Video')
        video()
        cv2.setWindowTitle('camKapture', 'camKapture')
    elif pressedKey == ord("b"): # press b to enter burst mode
        cv2.setWindowTitle('camKapture', 'camKapture - Burst')
        burst()
        cv2.setWindowTitle('camKapture', 'camKapture')
    elif pressedKey == ord("t"): # press t to enter timer mode
        cv2.setWindowTitle('camKapture', 'camKapture - Timer')
        count(10)
        cv2.setWindowTitle('camKapture', 'camKapture')
    elif pressedKey == 27: # Esc to exit
        break