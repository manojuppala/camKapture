import cv2

def blur(frame):
    return cv2.GaussianBlur(frame,(37,37),0)