#import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


class Obj_Detection():

    def __init__(self,vs,transmit):
    ### Setup ########################################################
        self.transmit = transmit
        self.vs = vs
        self.auto = 1
            #Construct the argument parse and parse the arguments
        '''    
        ap  = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
        self.args = vars(ap.parse_args())
        '''
#Define upper and lower bounds of color target and start buffer
        self.colorLower = (110,50,50)
        self.colorUpper = (130,255,255)
        #self.pts = deque(maxlen=self.args["buffer"])

#if a video path is not supplied, default to webcam
        '''       if not args.get("video", False):
            vs = cv2.VideoCapture(0)
#otherwise grab reference to video file
        else:
             vs = cv2.VideoCapture(args["video"])
        '''
#allow  camera/video to warm up
        #time.sleep(2.0)

### loop ########################################################

        self.flagseen = 0
### loop ########################################################

    def updateVid(self,frame):
        #ret, frame = self.vs.get_frame(0)
    #handle the frame from vidcap or vidstream
        #frame = frame[1] if self.args.get("video", False) else frame
    #if we dont get a frame, end of video
        if frame is None:
            return
    
    #resize the frame, blur, and convert to HSV color
    #frame = imutils.resize(frame, width=600)
        cv2.resize(frame, (0,0), fx=0.5,fy=0.5)
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #construct mask for color and use dilations&ersosions to reduce small noises
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
    
    
### Contour Draw ################################################
    #find contours in mask and find center(x,y) of the object
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        self.center = None
    
    #only proceed is at least one contour was found
        if len(cnts) > 0:
        #find largest contour in mask, use it to compute min circle and center
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            self.centerx = int(M["m10"] / M["m00"])

        #only proceed if the radius meets a minimum size
            if radius > 10:
            #draw circle and center on from and update trakced points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(frame, self.center, 5, (0,0,255), -1)
                self.flagseen = 1
            if radius > 120:
                self.transmit.send('x')
                self.stop = 1
            else:
                self.stop = 0
        '''    
    #update the points queue
        self.pts.appendleft(self.center)
    
    #loop over the set of tracked points
        for i in range(1, len(self.pts)):
        #if any tracked points are none, ignore them
            if self.pts[i-1] is None or self.pts[i] is None:
                continue
        #otherwise, compute thickness of line and draw lines
            thickness = int(np.sqrt(self.args["buffer"] / float(i+1))*2.5)
            cv2.line(frame, self.pts[i-1], self.pts[i], (0,0,255), thickness)
        '''
    ### Find Center of screen and compare with (x,y) of flag #############
    #screen = frame.shape
    #print(center)
    #print(centerx)
    #x, y = center 
        if (self.flagseen == 1) and (self.stop != 1):
            if self.centerx > 420:     #flag is right of center 340
                if self.auto == 1:
                    self.transmit.send('d')
                cv2.circle(frame, (500,240), 20, (0,0,255), 3)
            elif self.centerx < 220:   #flag is left of center 300
                if self.auto == 1:
                    self.transmit.send('a')
                cv2.circle(frame, (200,240), 20, (0,255,0), 3)
            elif 220 <= self.centerx <= 420: # 300 - 340
                if self.auto == 1:
                    self.transmit.send('w')
                cv2.circle(frame, (320,240), 20, (255,0,0), 3)
        else:
            print("no flag")        
    #cv2.circle(frame, (300,225), 20, (0,125,230), 3)
        cv2.line(frame, (320,0), (320,480), (255,0,0), 5)
        
    #display frame to screen
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    #if the 'q' key pressed, stop
    #    if key == ord("q"):
     #       break
####################################################################################################

### Ending #########################################################3
    def __del__(self):
#if not using a video file, stop cam video stream
        if not self.args.get("video", False):
            self.vs.stop()
#otherwise release cam
        else:
            self.vs.release()
#close all windows
        cv2.destroyAllWindows()