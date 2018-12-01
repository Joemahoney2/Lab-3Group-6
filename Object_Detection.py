#import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


class Obj_Detection():

    def __init__(self,vs,transmit,roverNum):
    ### Setup ########################################################
        self.transmit = transmit
        self.vs = vs
        self.auto = 1
        self.roverNum = roverNum

        # Define upper and lower bounds of color target and start buffer
        self.colorFlag1 = (110,50,50)
        self.colorFlag2 = (130,255,255)
        
        self.colorRover1 = (165,50,50)
        self.colorRover2 = (180,255,255)
        
        self.colorHome1 = (140,50,50)
        self.colorHome2 = (160,255,255)

        # allow  camera/video to warm up
        #time.sleep(2.0)
        self.flagPickup = 0
        self.coop = 1
        self.turns = 0
        self.noFlagTurn = 1
        self.flagSeen = 0
        self.flagHelper = 1
        self.flagApproachHelper = 1
        self.flagsRetrieved = 0
        self.headHome = 0

    # Driving instructions when no flag is seen
    def noFlag(self):
        
        self.flagSeen = 0
        self.flagPickup = 0
        print('Rover '+str(self.roverNum)+': no flag')
        if self.noFlagTurn == 0:
            self.transmit.send('w',self.roverNum)
        else:
            self.transmit.send('d',self.roverNum)
        
        '''
        if self.turns == 4:
            self.transmit.send('w')
            self.turns = 0
        else:
            self.turns += 1
            self.transmit.send('d')
        '''
    def updateVid(self,frame):

        if frame is None:
            return
        if self.auto == 0:
            return
    #resize the frame, blur, and convert to HSV color
    #frame = imutils.resize(frame, width=600)
        cv2.resize(frame, (0,0), fx=0.5,fy=0.5)
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #construct mask for color and use dilations&ersosions to reduce small noises
        mask1 = cv2.inRange(hsv, self.colorFlag1, self.colorFlag2)
        mask1 = cv2.erode(mask1, None, iterations=2)
        mask1 = cv2.dilate(mask1, None, iterations=2)
    
        mask2 = cv2.inRange(hsv, self.colorRover1, self.colorRover2)
        mask2 = cv2.erode(mask2, None, iterations=2)
        mask2 = cv2.dilate(mask2, None, iterations=2)
### Contour Draw ################################################
    #find contours in mask and find center(x,y) of the object
        cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = cnts1[0] if imutils.is_cv2() else cnts1[1]
        
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
        #self.center = None
        
        if self.headHome == 1: #self.flagsRetrieved >= 5:
            print('Go home')
           
            mask3 = cv2.inRange(hsv, self.colorHome1, self.colorHome2)
            mask3 = cv2.erode(mask3, None, iterations=2)
            mask3 = cv2.dilate(mask3, None, iterations=2)
### Contour Draw ################################################
    #find contours in mask and find center(x,y) of the object
            cnts3 = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts3 = cnts3[0] if imutils.is_cv2() else cnts3[1]
            
            if len(cnts3) > 0:
                c3 = max(cnts3, key=cv2.contourArea)
                ((x,y), radius3) = cv2.minEnclosingCircle(c3)
                M3 = cv2.moments(c3)
                #self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.centerx3 = int(M3["m10"] / M3["m00"])
                print(str(radius3))
                if radius3 > 25:
                    self.transmit.send('x',self.roverNum)
                if self.centerx3 > 420:     #flag is right of center 340
                    self.transmit.send('d',self.roverNum)
                    #print('Rover '+str(self.roverNum)+' sees only flag far away, on right')
                elif self.centerx3 < 220:   #flag is left of center 300
                    self.transmit.send('a',self.roverNum)
                    #print('Rover '+str(self.roverNum)+' sees only flag far away on left')
                elif 220 <= self.centerx3 <= 420: # 300 - 340
                    self.transmit.send('w',self.roverNum)
                    #print('Rover '+str(self.roverNum)+' sees only flag far away straight ahead')
            else:
                c3 = 0
                radius3 = 0
                self.noFlag()
                
    #only proceed is at least one contour was found
        #elif
        
        elif len(cnts1) > 0 or len(cnts2) > 0:
        #find largest contour in mask, use it to compute min circle and center
            
            # Sees Flag
            if len(cnts1) > 0:
                c = max(cnts1, key=cv2.contourArea)
                ((x,y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                #self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.centerx = int(M["m10"] / M["m00"])
            else:
                c = 0
                radius = 0#cv2.minEnclosingCircle(c)
                #M = cv2.moments(c)
                #self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #self.centerx = int(M["m10"] / M["m00"])
            
            # Sees Rover 
            if len(cnts2) > 0:
                c2 = max(cnts2, key=cv2.contourArea)
                ((x2,y2), radius2) = cv2.minEnclosingCircle(c2)
                M2 = cv2.moments(c2)
                #self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.centerx2 = int(M2["m10"] / M2["m00"])
            else:
                c2 = 0
                radius2 = 0
                
                #M2 = 0#cv2.moments(c2)
                #self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #self.centerx2 = 0#int(M2["m10"] / M2["m00"])
            
            # Rover 0: Turn always
            # Rover 1: Go for flag, otherwise turn
            if self.coop == 1 and self.roverNum == 0 and radius2 > 10: # Rover 0: Rover, maybe flag
                self.flagSeen = 1
                self.flagPickup = 0
                if self.centerx2 > 320:     #flag is right of center 340
                    self.transmit.send('a',self.roverNum)
                else:
                    self.transmit.send('d',self.roverNum)
                print('Coop, Rover 0 sees rover, maybe flag')
            elif self.coop == 1 and self.roverNum == 1 and radius2 > 10 and radius <= 10:  # Rover 1: Rover, no flag
                self.flagPickup = 0
                self.flagSeen = 1
                if self.centerx2 > 320:     #flag is right of center 340
                    self.transmit.send('a',self.roverNum)
                else:
                    self.transmit.send('d',self.roverNum)
                print('Coop, Rover 1 sees rover, no flag')
            elif self.coop == 0 and radius2 > 10 and radius <= 10:#COMPETITIVE MODE Rover, No flag
                self.flagSeen = 1
                self.flagPickup = 0
                print('Comp, Rover '+str(self.roverNum)+' sees rover, no flag')
                if self.centerx2 > 420:     #flag is right of center 340
                    self.transmit.send('d',self.roverNum)
                elif self.centerx2 < 220:   #flag is left of center 300
                    self.transmit.send('a',self.roverNum)
                elif 220 <= self.centerx2 <= 420: # 300 - 340
                    self.transmit.send('q',self.roverNum)

                
        #only proceed if the radius meets a minimum size
            # Position rover so flag is in center of screen for pickup
            elif radius > 80: #60 close 
                
                print('Rover '+str(self.roverNum)+' Pickup Radius: '+str(radius))
                self.flagApproachHelper = 1
                self.flagSeen = 1              
                
                if self.flagHelper == 0:
                    self.flagHelper = self.flagHelper + 1
                    
                    if self.centerx > 370:     #flag is right of center 340
                        self.transmit.send('d',self.roverNum)
                        print('Rover '+str(self.roverNum)+' sees only flag close on right')
                        print(str(self.centerx))
                        self.flagPickup = 0
                    elif (self.centerx < 270):# or (300 <= self.centerx <= 340):   #flag is left of center 300
                        self.transmit.send('a',self.roverNum)
                        self.flagPickup = 0
                        print('Rover '+str(self.roverNum)+' sees only flag close on left')
                        print(str(self.centerx))
                    elif 270 <= self.centerx <= 370:#(250 <= self.centerx < 300) or (340 <= self.centerx <= 380): # 300 - 340
                        self.transmit.send('f',self.roverNum)
                        self.flagsRetrieved = self.flagsRetrieved + 1
                        self.flagPickup = 1
                        
                elif self.flagHelper >= 4:
                    self.flagHelper = 0
                    self.transmit.send('x',self.roverNum)
                    print('Rover '+str(self.roverNum)+' reset flagHelper. FlagHelper: ' +str(self.flagHelper))
                else:
                    self.flagHelper = self.flagHelper + 1
                    self.transmit.send('x',self.roverNum)
                    print('Rover '+str(self.roverNum)+' incrementing flagHelper. FlagHelper: ' +str(self.flagHelper))
                    
                
            elif radius > 35: #60 close 
                
                self.flagSeen = 1              
                self.flagHelper = 1
                
                if self.flagApproachHelper == 0:
                    self.flagApproachHelper = self.flagApproachHelper + 1
                    
                    if radius <= 80:     #flag is right of center 340
                        self.transmit.send('w',self.roverNum)
                        print('Rover '+str(self.roverNum)+' approaching flag')
                        print(str(radius))
                        self.flagPickup = 0
                    
                        
                elif self.flagApproachHelper >= 3:
                    self.flagApproachHelper = 0
                    self.transmit.send('x',self.roverNum)
                    print('Rover '+str(self.roverNum)+' reset flagApproachHelper. FlagApproachHelper: ' +str(self.flagApproachHelper))
                else:
                    self.flagApproachHelper = self.flagApproachHelper + 1
                    self.transmit.send('x',self.roverNum)
                    print('Rover '+str(self.roverNum)+' incrementing flagApproachHelper. FlagApproachHelper: ' +str(self.flagApproachHelper))
            
            
            # Normal driving when flag seen
            elif radius > 10:
                
                self.flagApproachHelper = 1
                self.flagHelper = 1
                self.flagSeen = 1
                self.flagPickup = 0
                if self.centerx > 420:     #flag is right of center 340
                    self.transmit.send('d',self.roverNum)
                    print('Rover '+str(self.roverNum)+' sees only flag far away, on right')
                elif self.centerx < 220:   #flag is left of center 300
                    self.transmit.send('a',self.roverNum)
                    print('Rover '+str(self.roverNum)+' sees only flag far away on left')
                elif 220 <= self.centerx <= 420: # 300 - 340
                    self.transmit.send('w',self.roverNum)
                    print('Rover '+str(self.roverNum)+' sees only flag far away straight ahead')
            
            # No flag seen
            else:
                self.noFlag()
        # No flag seen
        else:
            self.noFlag()
                
    #display frame to screen
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

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