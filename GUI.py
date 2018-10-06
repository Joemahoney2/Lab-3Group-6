import tkinter
from tkinter import font
from PIL import Image
from PIL import ImageTk
#from tkinter.ttk import Frame, Button, Style
from tkinter import *

winWidth = 0
winHeight = 0
manualButton = 0
autoButton = 0
coopButton = 0
compButton = 0
inst1Text = 0
inst2Text = 0

class GUI(Frame):
  
    def __init__(self):
        super().__init__()
         
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
    
    def manualPressed(self):
        
        self.buttonDown(down = manualButton, up = autoButton)
        coopButton.pack_forget()
        compButton.pack_forget()
        inst1Text.pack(fill=BOTH, expand=1)
        inst2Text.pack(fill=BOTH, expand=1)
        
    def coopPressed(self):
        
        self.buttonDown(down = coopButton, up = compButton)
        
    def compPressed(self):
        
        self.buttonDown(down = compButton, up = coopButton)
                
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

####################################### TEXT INSTRUCTIONS #######################################        
        
        inst1Frame = Frame(self, height=int(.346*winHeight), width=int(.162*winWidth))
        inst1Frame.pack_propagate(0) # don't shrink
        inst1Frame.place(x = 400, y = int(.63*winHeight))
                
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
        inst2Frame.place(x = 400+2*int(.14*winWidth), y = int(.63*winHeight))
                
        global inst2Text
        inst2Text = Button(inst2Frame, text="Rover 2 driving directions:\n  up arrow: forward\n  left arrow: left\n  back arrow: backward\n  right arrow: right\n  p: flag pickup")
        inst2Text.pack(fill=BOTH, expand=1)
        inst2Text.bind('<Button-2>', lambda e: 'break')

        inst2Text['font'] = helv14
        inst2Text['justify'] = LEFT
        inst2Text['anchor'] = NW
        inst2Text['relief'] = FLAT
        
        inst2Text.pack_forget()
        
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


        
def main():
  
    root = Tk()
    
    app = GUI()
    root.mainloop()  


if __name__ == '__main__':
    main()  