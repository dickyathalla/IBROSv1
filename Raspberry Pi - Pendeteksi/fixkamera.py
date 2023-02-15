import cv2
import sys

cpt = 0
bts = 5 # if you want 5 frames only.
vidStream = cv2.VideoCapture(0) # index of your camera
ret, frame = vidStream.read()

def cam():
    global cpt
    ret, frame = vidStream.read() # read frame and return code.
    if not ret: # if return code is bad, abort.
        sys.exit(0)
    cv2.imwrite("/home/pi/coba/gambar ke %04i.jpg" %cpt, frame)
    cpt += 1
   
while cpt<bts:
    cam()
    
