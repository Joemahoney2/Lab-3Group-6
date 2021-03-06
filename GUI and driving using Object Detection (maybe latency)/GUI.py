import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from tkinter import font
from PIL import Image
from PIL import ImageTk
from tkinter import *
import Top


'''
    TODO:
    	Send key press/release info to Top
    	Send button click info to Top (auto, manual, coop, and competitive)
    	Receive Label update info from Top
    	
    	Import video sources and bluetooth destinations from top module

'''
#keyHit = 'x'
class GUI(Frame):
  
    def __init__(self, transmit, vid, vid2, OD1):
        super().__init__()
        self.transmit = transmit 
        self.vid = vid
        self.vid2 = vid2
        self.OD1 = OD1
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
    
    def manualPressed(self):
        
        self.buttonDown(down = manualButton, up = autoButton)
        coopButton.pack_forget()
        compButton.pack_forget()
        inst1Text.pack(fill=BOTH, expand=1)
        inst2Text.pack(fill=BOTH, expand=1)
        self.manualMode = 1
        self.OD1.auto = 0
        
    def coopPressed(self):
        
        self.buttonDown(down = coopButton, up = compButton)
        
    def compPressed(self):
        
        self.buttonDown(down = compButton, up = coopButton)
    
    def keyPressed(self,event):
        
        if(not self.manualMode):
           return
       # global keyHit
        keyHit = event.keysym
        if(keyHit=='a'):
           print('a')
           self.transmit.send('a')
        elif(keyHit=='w'):
           print('w')
           self.transmit.send('w')
        elif(keyHit=='s'):
           print('s')
           self.transmit.send('s')
        elif(keyHit=='d'):
           print('d')
           self.transmit.send('d')
        elif(keyHit=='f'):
           print('f')
           self.transmit.send('f')
        elif(keyHit=='p'):
           print('p')
        #   self.transmit.send('p')
        elif(keyHit=='Left'):
           print('left arrow')
        #   self.transmit.send('w')
        elif(keyHit=='Right'):
           print('right arrow')
        elif(keyHit=='Up'):
           print('up arrow')
        elif(keyHit=='Down'):
           print('down arrow')
        else:
           print('none')
           
    def keyReleased(self,event):
        
        if(not self.manualMode):
           return
        keyHit = event.keysym
        if(keyHit=='a'):
           print('a released')
        elif(keyHit=='w'):
           print('w released')         
        elif(keyHit=='s'):
           print('s released')
        elif(keyHit=='d'):
           print('d released')
        elif(keyHit=='f'):
           print('f released')
        elif(keyHit=='p'):
           print('p released')
        elif(keyHit=='Left'):
           print('left arrow released')
        elif(keyHit=='Right'):
           print('right arrow released')
        elif(keyHit=='Up'):
           print('up arrow released')
        elif(keyHit=='Down'):
           print('down arrow released')
        else:
           print('none released')
        self.transmit.send('x')
                       
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
        
        flag1Frame = Frame(self, height=int(.05*winHeight), width=int(.162*winWidth))
        flag1Frame.pack_propagate(0) # don't shrink
        flag1Frame.place(x = 400, y = int(.64*winHeight))
                
        global flag1Text
        flag1Text = Label(flag1Frame, text="Flags retrieved: 0")
        flag1Text.pack(fill=BOTH, expand=1)
        
        helv16 = font.Font(family='Helvetica', size=16, weight = 'bold')
        
        flag1Text['font'] = helv16
        flag1Text['justify'] = LEFT
        
        flag2Frame = Frame(self, height=int(.05*winHeight), width=int(.162*winWidth))
        flag2Frame.pack_propagate(0) # don't shrink
        flag2Frame.place(x = 400+2*int(.12*winWidth), y = int(.64*winHeight))
                
        global flag2Text
        flag2Text = Label(flag2Frame, text="Flags retrieved: 0")
        flag2Text.pack(fill=BOTH, expand=1)
        
        flag2Text['font'] = helv16
        flag2Text['justify'] = LEFT
        
####################################### COOP BUTTON #############################################        
        
        coopFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        coopFrame.pack_propagate(0) # don't shrink
        coopFrame.place(x = int(winWidth-.208*winWidth-100), y = int(.66*winHeight))
                
        global coopButton
        coopButton = Button(coopFrame, text="Cooperative Mode", command=self.coopPressed)
        coopButton.pack(fill=BOTH, expand=1)        

        coopButton['font'] = helv18
        coopButton['bg'] = 'gray'

####################################### COMP BUTTON #############################################        
        
        compFrame = Frame(self, height=int(.107*winHeight), width=int(.208*winWidth))
        compFrame.pack_propagate(0) # don't shrink
        compFrame.place(x = int(winWidth-.208*winWidth-100), y = int(.78*winHeight))
                
        global compButton
        compButton = Button(compFrame, text="Competitive Mode", command=self.compPressed)
        compButton.pack(fill=BOTH, expand=1)        

        compButton['font'] = helv18
        compButton['bg'] = 'red'
        compButton['relief'] = SUNKEN
        
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
        
        self.delay = 15
        self.vidupdate()
        #self.transmit.close()
        
        
    def vidupdate(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame(1)
        ret2, frame2 = self.vid2.get_frame(1)

        
        # *** Inside these if statements we need reference back to Object_Detection code to update *** # 
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.OD1.updateVid()
        if ret2:
            self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
            self.canvas2.create_image(0, 0, image = self.photo2, anchor = tkinter.NW)
 
        self.vidFrame.after(self.delay, self.vidupdate)
        
