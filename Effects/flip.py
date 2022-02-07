import cv2

def flip_vertical(frame):
    return cv2.flip(frame, 1)

def flip_horizontal(frame):
    return cv2.flip(frame, 0)