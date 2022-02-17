import cv2

def edge(frame):
    return cv2.Canny(frame, 150,200)