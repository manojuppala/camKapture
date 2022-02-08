import cv2
from .flip import flip_vertical, flip_horizontal

effects=[flip_vertical, flip_horizontal]

# func to switch between different effects
def show_effect(cap,showeffect):
    k=0
    while True:
        success, frame1 = cap.read()
        frame1 = effects[k](frame1)
        cv2.imshow('camKapture',frame1) 
        pressedKey = cv2.waitKeyEx(1) & 0xFF
        if pressedKey == ord("e"): 
            showeffect = not showeffect 
            return showeffect,effects[k]
        elif pressedKey == ord("}"): k=k+1
        elif pressedKey == ord("{"): k=k-1
        elif pressedKey == 8:
            showeffect = not showeffect 
            return showeffect,[]

        k = 0 if k==len(effects) else abs(k)