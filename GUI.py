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
    
    def manualPressed(self):
        
        self.buttonDown(down = manualButton, up = autoButton)
        
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
        

def main():
  
    root = Tk()
    
    app = GUI()
    root.mainloop()  


if __name__ == '__main__':
    main()  