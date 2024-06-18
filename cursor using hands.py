import cv2
from cvzone.HandTrackingModule import HandDetector
import mouse
import numpy as np
import threading
import time

detector=HandDetector(detectionCon=0.9,maxHands=1)




print(cv2.__version__)
width=640
height= 360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) #camera object # DSHOW : DIRECT SHOW TO MAKE CAMERA LOAD FASTER

cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # setting everything do that it runs smoothly on windows

framereduction=100 # to solve prob of jittering of hand detection at extremes of webcam window

l_delay=0
r_delay=0
d_delay=0
def lclick_delay():
    global l_delay
    global lclick_thread
    time.sleep(1)
    l_delay=0
    lclick_thread=threading.Thread(target=lclick_delay)

lclick_thread=threading.Thread(target=lclick_delay)

def rclick_delay():
    global r_delay
    global rclick_thread
    time.sleep(1)
    r_delay=0
    rclick_thread=threading.Thread(target=rclick_delay)

rclick_thread=threading.Thread(target=rclick_delay)

def dclick_delay():
    global d_delay
    global dclick_thread
    time.sleep(1)
    d_delay=0
    dclick_thread=threading.Thread(target=dclick_delay)

dclick_thread=threading.Thread(target=dclick_delay)

while True:
    ignore, frame = cam.read() # read a frame
    frame=cv2.flip(frame,1)

    hands,frame=detector.findHands(frame,flipType=False)

    cv2.rectangle(frame,(framereduction,framereduction),(int(width-framereduction),int(height-framereduction)),(0,255,0),2)
    

    if hands:
        landmarklist=hands[0]['lmList']
        indxpos=landmarklist[8][0]
        indypos=landmarklist[8][1]

        midxpos,midypos=landmarklist[12][0],landmarklist[12][1]

        cv2.circle(frame,(indxpos,indypos),10,(0,255,0),-1)

        fingersopen=detector.fingersUp(hands[0]) # array of len 5 with values 0 or 1; 1-open 0-closed
        #all open==> [0,1,1,1,1] as we've used cv2.flip
        #all closed==> [1,0,0,0,0] as we've used cv2.flip
        print(fingersopen)

       

        if fingersopen[1]==1 and fingersopen[2]==0 and fingersopen[0]==1:
             conv_x=int(np.interp(indxpos,[framereduction,width-framereduction],[0,1280]))
             conv_y=int(np.interp(indypos,[framereduction,height-framereduction],[0,720]))  # interpolate the values from index position to range and height of the screen 

             mouse.move(conv_x,conv_y)
 # click function
        if fingersopen[1]==1 and fingersopen[2]==1 and fingersopen[0]==1:
            if abs(midxpos-indxpos)<30:
                if l_delay==0 and fingersopen[4]==0:
                    mouse.click(button="left")
                    l_delay=1
                    lclick_thread.start()

            if abs(midxpos-indxpos)<20:

                if r_delay==0 and fingersopen[4]==1:
                    mouse.click(button="right")
                    r_delay=1
                    rclick_thread.start()

#scroll function

#double click function

        if fingersopen[1]==1 and fingersopen[2]==0 and fingersopen[0]==0 and fingersopen[4]==0:
            if d_delay==0:
                mouse.double_click(button="left")
                d_delay=1
                dclick_thread.start()







    
    cv2.resize(frame,(width,height))
    cv2.imshow('mycam1',frame) # show a frame
    cv2.moveWindow('mycam1',0,0)

    #print(frame)

    if cv2.waitKey(1) & 0xff == ord(' '):  # key to be pressed to exit 
        break

cam.release()

