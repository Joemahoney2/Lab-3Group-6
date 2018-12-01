import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from tkinter import font
from PIL import Image
from PIL import ImageTk
from tkinter import *
import Top
import signal


'''
    TODO:
    	DONE Send key press/release info to Top
    	Send button click info to Top (auto, manual, coop, and competitive)
    	Receive Label update info from Top
    	
    	DONE Import video sources and bluetooth destinations from top module

'''
#keyHit = 'x'
class GUI(Frame):
  
    def __init__(self, root, transmit1, transmit2, vid, vid2, OD1, OD2):
        super().__init__()
        self.root = root
        self.transmit1 = transmit1 
        self.transmit2 = transmit2
        self.vid = vid
        self.vid2 = vid2
        self.OD1 = OD1
        self.OD2 = OD2
        self.flags1 = 0
        self.flagCounted1 = 0
        self.flags2 = 0
        self.flagCounted2 = 0
        self.roverTimer1 = 0
        self.roverTimer2 = 0
        self.initUI()
       
    def buttonDown(self, down, up):
        down['relief'] = SUNKEN
        down['bg'] = 'red'
        up['relief'] = RAISED
        up['bg'] = 'gray'
    
    def autoPressed(self):
        
        self.buttonDown(down = autoButton, up = manualButton)
        coopButton.pack(fill=BOTH, expand=1)
        compButton.pack(fill=BOTH, expand=1)
        inst1Text.pack_forget()
        inst2Text.pack_forget()
        self.manualMode = 0
        self.OD1.auto = 1
        self.OD2.auto = 1
    
    def manualPressed(self):
        
        self.buttonDown(down = manualButton, up = autoButton)
        coopButton.pack_forget()
        compButton.pack_forget()
        inst1Text.pack(fill=BOTH, expand=1)
        inst2Text.pack(fill=BOTH, expand=1)
        self.manualMode = 1
        self.OD1.auto = 0
        self.OD2.auto = 0
        
    def coopPressed(self):
        
        self.buttonDown(down = coopButton, up = compButton)
        self.OD1.coop = 1
        self.OD2.coop = 1
        
    def compPressed(self):
        
        self.buttonDown(down = compButton, up = coopButton)
        self.OD1.coop = 0
        self.OD2.coop = 0
    
    def homeDown(self, down):
        down['relief'] = SUNKEN
        down['bg'] = 'red'
        
    def homePressed(self):
        
        self.homeDown(down = homeButton)
        self.OD1.headHome = 1
        self.OD2.headHome = 1
    
    def keyPressed(self,event):
        
        if(not self.manualMode):
            return
        # global keyHit
        keyHit = event.keysym
        if(keyHit=='a'):
            print('a')
            self.transmit1.send('a',0)
            print('a sent')
        elif(keyHit=='w'):
            print('w')
            self.transmit1.send('w',0)
            print('w sent')
        elif(keyHit=='s'):
            print('s')
            self.transmit1.send('s',0)
            print('s sent')
        elif(keyHit=='d'):
            print('d')
            self.transmit1.send('d',0)
            print('d sent')
        elif(keyHit=='f'):
            print('f')
            self.transmit1.send('f',0)
            print('f sent')
        elif(keyHit=='p'):
            print('p')
            self.transmit2.send('p',0)
            print('p sent')
        elif(keyHit=='Left'):
            print('j - left arrow')
            self.transmit2.send('j',0)
            print('j sent')
        elif(keyHit=='Right'):
            print('l - right arrow')
            self.transmit2.send('l',0)
            print('l sent')
        elif(keyHit=='Up'):
            print('i - up arrow')
            self.transmit2.send('i',0)
            print('i sent')
        elif(keyHit=='Down'):
            print('k - down arrow')
            self.transmit2.send('k',0)
            print('k sent')
        else:
            print('none')
           
    def keyReleased(self,event):
        
        if(not self.manualMode):
            return
        keyHit = event.keysym
        if(keyHit=='a'):
            print('a released')
            self.transmit1.send('x',0)
        elif(keyHit=='w'):
            print('w released')
            self.transmit1.send('x',0)         
        elif(keyHit=='s'):
            print('s released')
            self.transmit1.send('x',0)
        elif(keyHit=='d'):
            print('d released')
            self.transmit1.send('x',0)
        elif(keyHit=='f'):
            print('f released')
            self.flags1 = self.flags1 + 1;
            self.flag1Text['text'] = "Flags retrieved: "+str(self.flags1)
            self.transmit1.send('x',0)
        elif(keyHit=='p'):
            print('p released')
            self.flags2 = self.flags2 + 1;
            self.flag2Text['text'] = "Flags retrieved: "+str(self.flags2)
            self.transmit2.send('m',0)
        elif(keyHit=='Left'):
            print('left arrow released')
            self.transmit2.send('m',0)
        elif(keyHit=='Right'):
            print('right arrow released')
            self.transmit2.send('m',0)
        elif(keyHit=='Up'):
            print('up arrow released')
            self.transmit2.send('m',0)
        elif(keyHit=='Down'):
            print('down arrow released')
            self.transmit2.send('m',0)
        else:
            print('none released')
        print('x or m sent')
        #self.transmit.send('x',0)
                       
    def initUI(self):
      
        self.master.title("Robot Flag Finders")
        self.pack(fill=BOTH, expand=1)
        winWidth = self.master.winfo_screenwidth()
        winHeight = self.master.winfo_screenheight()
        self.master.geometry('%dx%d+-10+0' % (winWidth,winHeight)) #1400x700


#######################################  MANUAL BUTTON ######################################        
        manualFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        manualFrame.pack_propagate(0) # don't shrink
        manualFrame.place(x = 100, y = int(.66*winHeight))
                
        global manualButton        
        manualButton = Button(manualFrame, text="Manual Mode", command=self.manualPressed)
        manualButton.pack(fill=BOTH, expand=1)
        
        helv18 = font.Font(family='Helvetica', size=18, weight='bold')
        manualButton['font'] = helv18
        manualButton['bg'] = 'gray'

#######################################  AUTONOMOUS BUTTON ######################################        
        autoFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        autoFrame.pack_propagate(0) # don't shrink
        autoFrame.place(x = 100, y = int(.78*winHeight))
                
        global autoButton
        autoButton = Button(autoFrame, text="Autonomous Mode", command=self.autoPressed)
        autoButton.pack(fill=BOTH, expand=1)        

        autoButton['font'] = helv18
        autoButton['bg'] = 'red'
        autoButton['relief'] = SUNKEN
        
        self.manualMode = 0

####################################### TEXT INSTRUCTIONS #######################################        
        
        inst1Frame = Frame(self, height=int(.346*winHeight), width=int(.162*winWidth))
        inst1Frame.pack_propagate(0) # don't shrink
        inst1Frame.place(x = 400, y = int(.7*winHeight))
                
        global inst1Text
        inst1Text = Button(inst1Frame, text="Rover 1 driving directions:\n  w: forward\n  a: left\n  s: backward\n  d: right\n  f: flag pickup")
        inst1Text.pack(fill=BOTH, expand=1)
        inst1Text.bind('<Button-1>', lambda e: 'break')
        
        helv14 = font.Font(family='Helvetica', size=14)

        inst1Text['font'] = helv14
        inst1Text['justify'] = LEFT
        inst1Text['anchor'] = NW
        inst1Text['relief'] = FLAT
        
        inst1Text.pack_forget()
        
        inst2Frame = Frame(self, height=int(.346*winHeight), width=int(.162*winWidth))
        inst2Frame.pack_propagate(0) # don't shrink
        inst2Frame.place(x = 400+2*int(.12*winWidth), y = int(.7*winHeight))
                
        global inst2Text
        inst2Text = Button(inst2Frame, text="Rover 2 driving directions:\n  up arrow: forward\n  left arrow: left\n  back arrow: backward\n  right arrow: right\n  p: flag pickup")
        inst2Text.pack(fill=BOTH, expand=1)
        inst2Text.bind('<Button-1>', lambda e: 'break')

        inst2Text['font'] = helv14
        inst2Text['justify'] = LEFT
        inst2Text['anchor'] = NW
        inst2Text['relief'] = FLAT
        
        inst2Text.pack_forget()
        
####################################### FLAG TEXT ###############################################
        
        self.flag1Frame = Frame(self, height=int(.05*winHeight), width=int(.162*winWidth))
        self.flag1Frame.pack_propagate(0) # don't shrink
        self.flag1Frame.place(x = 400, y = int(.64*winHeight))
                
        #global flag1Text
        self.flag1Text = Label(self.flag1Frame, text="Flags retrieved: 0")
        self.flag1Text.pack(fill=BOTH, expand=1)
        
        helv16 = font.Font(family='Helvetica', size=16, weight = 'bold')
        
        self.flag1Text['font'] = helv16
        self.flag1Text['justify'] = LEFT
        
        self.flag2Frame = Frame(self, height=int(.05*winHeight), width=int(.162*winWidth))
        self.flag2Frame.pack_propagate(0) # don't shrink
        self.flag2Frame.place(x = 400+2*int(.12*winWidth), y = int(.64*winHeight))
                
        #global flag2Text
        self.flag2Text = Label(self.flag2Frame, text="Flags retrieved: 0")
        self.flag2Text.pack(fill=BOTH, expand=1)
        
        self.flag2Text['font'] = helv16
        self.flag2Text['justify'] = LEFT
        
####################################### HOME BUTTON #############################################

        homeFrame = Frame(self, height=int(.05*winHeight), width=int(.09*winWidth))
        homeFrame.pack_propagate(0) # don't shrink
        homeFrame.place(x = int(winWidth/2 - .06*winWidth), y = int(.64*winHeight))
                
        global homeButton
        homeButton = Button(homeFrame, text="Go Home", command=self.homePressed)
        homeButton.pack(fill=BOTH, expand=1)        

        helv16 = font.Font(family='Helvetica', size=16, weight = 'bold')
        homeButton['font'] = helv16
        homeButton['bg'] = 'gray'
        
####################################### COOP BUTTON #############################################        
        
        coopFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        coopFrame.pack_propagate(0) # don't shrink
        coopFrame.place(x = int(winWidth-.208*winWidth-100), y = int(.66*winHeight))
                
        global coopButton
        coopButton = Button(coopFrame, text="Cooperative Mode", command=self.coopPressed)
        coopButton.pack(fill=BOTH, expand=1)        

        coopButton['font'] = helv18
        coopButton['bg'] = 'red'
        coopButton['relief'] = SUNKEN
        
       

####################################### COMP BUTTON #############################################        
        
        compFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        compFrame.pack_propagate(0) # don't shrink
        compFrame.place(x = int(winWidth-.208*winWidth-100), y = int(.78*winHeight))
                
        global compButton
        compButton = Button(compFrame, text="Competitive Mode", command=self.compPressed)
        compButton.pack(fill=BOTH, expand=1)        

        compButton['font'] = helv18
        compButton['bg'] = 'gray'
        
####################################### VIDEO STREAM #############################################        
        
        # https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
        
        ##### ENTER URL ##### (webcam = 1)
        self.video_source = 1; 
        #####################
        
        #self.vid = Top.VideoStream(self.video_source)
        self.vidFrame = Frame(self, height=self.vid.height, width=self.vid.width)
        self.vidFrame.pack_propagate(0) # don't shrink
        self.vidFrame.place(x = 30, y = 10)
               
        self.canvas = tkinter.Canvas(self.vidFrame, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
        
        ##### ENTER URL ##### (webcam = 1)
        self.video_source2 = 0#'http://admin:admin@10.161.76.129:8081' #'http://admin:admin@192.168.0.4:8081/' 
        #####################
        
        #self.vid2 = Top.VideoStream(self.video_source2)
        self.vid2Frame = Frame(self, height=self.vid2.height, width=self.vid2.width)
        self.vid2Frame.pack_propagate(0) # don't shrink
        self.vid2Frame.place(x = winWidth/2, y = 10)
               
        self.canvas2 = tkinter.Canvas(self.vid2Frame, width = self.vid2.width, height = self.vid2.height)
        self.canvas2.pack()
        
        #self.transmit = Top.BT()
        #### REPSOND TO KEYBOARD INPUT ####
        
        self.bind_all("<Key>",self.keyPressed)
        self.bind_all("<KeyRelease>",self.keyReleased)
        
        ###################################
        
        self.delay = 45
        self.vidupdate()
        #self.transmit.close()
        
        
    def vidupdate(self):
        # Get a frame from the video source
        #print('Get Vid 1 frame')
        
        self.frame = self.vid.get_frame()
        #print('Get Vid 2 frame')
        self.frame2 = self.vid2.get_frame()
        
        
        
        # Approximate Timer for controlling rover when no flag seen
        #print('Check for no flag seen')
        if self.roverTimer1 >= 10: # 3 secs
            self.roverTimer1 = 0
            if self.OD1.noFlagTurn == 0:
                self.OD1.noFlagTurn = 1
            else:
                self.OD1.noFlagTurn = 0
        elif self.OD1.flagSeen == 0:
            self.roverTimer1 = self.roverTimer1 + 1
        else:
            self.roverTimer1 = 0
        
        # Approximate Timer for controlling rover when no flag seen
        if self.roverTimer2 >= 10: # 3 secs
            self.roverTimer2 = 0
            if self.OD2.noFlagTurn == 0:
                self.OD2.noFlagTurn = 1
            else:
                self.OD2.noFlagTurn = 0
        elif self.OD2.flagSeen == 0:
            self.roverTimer2 = self.roverTimer2 + 1
        else:
            self.roverTimer2 = 0
        
        #print('Update flag labels')
        # Update Flag Label in Autonomous Mode
        if self.OD1.flagPickup == 1 and self.flagCounted1 == 0 and self.manualMode == 0:
            self.flagCounted1 = 1
            self.flags1 = self.flags1 + 1
            self.flag1Text['text'] = "Flags retrieved: " + str(self.flags1)
        elif self.OD1.flagPickup == 0:
            self.flagCounted1 = 0
        
        # Update Flag Label in Autonomous Mode
        if self.OD2.flagPickup == 1 and self.flagCounted2 == 0 and self.manualMode == 0:
            self.flagCounted2 = 1
            self.flags2 = self.flags2 + 1
            self.flag2Text['text'] = "Flags retrieved: " + str(self.flags2)
        elif self.OD2.flagPickup == 0:
            self.flagCounted2 = 0		
        
        
        #print('Display frame 1 on GUI')
        # *** Inside these if statements we need reference back to Object_Detection code to update *** # 
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.OD1.updateVid(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
        
        #print('Display frame 2 on GUI')
        self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame2))
        self.canvas2.create_image(0, 0, image = self.photo2, anchor = tkinter.NW)#
        self.OD2.updateVid(cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB))
        
        #print('update_idle_tasks()')
        self.root.update_idletasks()
        #print('end of update')
        self.vidFrame.after(self.delay, self.vidupdate) # self.delay,
