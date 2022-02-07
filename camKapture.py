# camKapture is an open source application that allows users to access their webcam device and take pictures or create videos.
import cv2, math, numpy as np, os
from datetime import datetime
from Effects import flip

# path to write image and video files.
img_directory = os.path.expanduser('~')+r'/Pictures/camKapture/'
vid_directory = os.path.expanduser('~')+r'/Videos/camKapture/'

if not os.path.exists(img_directory): os.mkdir(img_directory)
if not os.path.exists(vid_directory): os.mkdir(vid_directory)

fullscreen=False
showeffect=False
effects=[flip.flip_vertical, flip.flip_horizontal]
current_effect = []

# func to switch between different effects
def show_effect(cap):
    global showeffect, effects
    k=0
    while True:
        success, frame1 = cap.read()
        frame1 = effects[k](frame1)
        cv2.imshow('camKapture',frame1)
        pressedKey = cv2.waitKeyEx(1) & 0xFF
        if pressedKey == ord("e"): 
            showeffect = not showeffect 
            return effects[k]
        elif pressedKey == ord("}"): k=k+1
        elif pressedKey == ord("{"): k=k-1
        elif pressedKey == 8:
            showeffect = not showeffect 
            return []
        if k==len(effects): k=0
        elif k<0: k=abs(k)

# a flash screen that appears every time a frame is saved
def white_screen():
    frame=np.zeros([100,100,3],dtype=np.uint8)
    frame.fill(255)
    cv2.imshow('camKapture',frame)
    cv2.waitKey(100)

# this func displays text on a the image or video
def text_display(frame,type,text,coordinates=(0,0),fontScale=0,color=(255,255,255),thickness=0):
    font=cv2.FONT_HERSHEY_SIMPLEX
    if type=='top':
        coordinates=(0,20)
        fontScale=0.6
        color=(0,0,255)
        thickness=1
    elif type=='center':
        coordinates=(300,250)
        fontScale=2
        color=(255,255,255)
        thickness=3
    cv2.putText(frame,text,coordinates,font,fontScale,(0,0,0),thickness+2,cv2.LINE_AA)
    cv2.putText(frame,text,coordinates,font,fontScale,color,thickness,cv2.LINE_AA)

# this func triggers a count of 10secs before a frame is saved.
def count(n,cap):
    j=(n+1)*10-1
    while True:
        success, frame1 = cap.read()
        success, frame2 = cap.read()
        cv2.imshow('camKapture', frame1)
        if j>=10:
            text=str(math.floor(j/10)) 
            text_display(frame2,'custom',text,(400,250),4,(255,255,255),5)
            cv2.imshow('camKapture', frame2)
            cv2.waitKeyEx(100)
            j=j-1
        else:
            cv2.imshow('camKapture', frame1)
            cv2.imwrite(os.path.join(img_directory , str(datetime.now())+'.jpg'),frame1)
            white_screen()
            print('Image saved to '+os.path.join(img_directory , str(datetime.now())+'.jpg'))
            return

def burst(cap):
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

def video(cap):
    global fullscreen, showeffect, effects
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    result = cv2.VideoWriter(os.path.join(vid_directory , str(datetime.now())+'.avi'),fourcc,20, size)
    unpaused=True

    while True:
        success, frame = cap.read()
        pressedKey = cv2.waitKeyEx(1) & 0xFF

        if current_effect:
            frame=current_effect(frame)

        if success == True: 
            if(unpaused):
                result.write(frame)
                text_display(frame,'top','Recording...')
            else:
                text_display(frame,'center','paused')
            cv2.imshow('camKapture', frame)
            
            if fullscreen:
                cv2.setWindowProperty("camKapture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            else:
                cv2.resizeWindow('camKapture',854,480)

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
            elif pressedKey == 32: # Space to pause and unpause
                unpaused= not unpaused
            elif pressedKey == ord("f"): # press t to enter fullscreen mode
                fullscreen=not fullscreen
        else:
            break

def main():
    cap= cv2.VideoCapture(0)
    cap.set(3,854)
    cap.set(4,480)
    global fullscreen, showeffect, effects, current_effect
    
    while True:
        success, frame = cap.read()
        cv2.namedWindow('camKapture', flags=cv2.WINDOW_GUI_NORMAL)
        if showeffect: 
            cv2.setWindowTitle('camKapture', 'camKapture - Effects')
            current_effect = show_effect(cap)
            cv2.setWindowTitle('camKapture', 'camKapture')
        if current_effect:
            frame=current_effect(frame)
        cv2.imshow('camKapture',frame)

        if fullscreen:
            cv2.setWindowProperty("camKapture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.resizeWindow('camKapture',854,480)
            
        pressedKey = cv2.waitKeyEx(1) & 0xFF

        if pressedKey == ord("s"): # press s to save a frame
            cv2.imwrite(os.path.join(img_directory , str(datetime.now())+'.jpg'),frame)
            white_screen()
            print('Image saved to '+os.path.join(img_directory , str(datetime.now())+'.jpg'))
        elif pressedKey == ord("v"): # press v to enter video mode
            cv2.setWindowTitle('camKapture', 'camKapture - Video')
            video(cap)
            cv2.setWindowTitle('camKapture', 'camKapture')
        elif pressedKey == ord("b"): # press b to enter burst mode
            cv2.setWindowTitle('camKapture', 'camKapture - Burst')
            burst(cap)
            cv2.setWindowTitle('camKapture', 'camKapture')
        elif pressedKey == ord("t"): # press t to enter timer mode
            cv2.setWindowTitle('camKapture', 'camKapture - Timer')
            count(10,cap)
            cv2.setWindowTitle('camKapture', 'camKapture')
        elif pressedKey == ord("f"): # press f to enter fullscreen mode
            fullscreen = not fullscreen
        elif pressedKey == ord("e"): # press e to enter effects mode
            showeffect = not showeffect
        elif pressedKey == 27: # Esc to exit
            break
    return

if __name__=="__main__":
    main()