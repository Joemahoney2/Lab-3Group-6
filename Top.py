import GUI
import Object_Detection
import bluetooth
#import imutils
#from imutils.video import VideoStream
#import tkinter
import cv2
#import PIL.Image
#import PIL.ImageTk
#from tkinter import font
#from PIL import Image
#from PIL import ImageTk
from tkinter import *
import time
import subprocess
import re
from threading import Thread
from PIL import Image
import requests
from io import BytesIO
from urllib import *
import numpy

class BT():
    def __init__(self, serverMACAddress = '98:D3:11:FC:19:4C', port=1):
        #serverMACAddress = '98:D3:11:FC:19:4C'
        self.port = port
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Trying to connect')
        self.s.connect((serverMACAddress, port))
        print('Connected')
    def send(self,data):
        self.s.send(data)
    def close(self):
        self.s.close()

class VideoStream2:
    def __init__(self, video_source=1):
        self.video_source = video_source
        
        # Get video source width and height
        
        time.sleep(2.0)
        if(self.video_source != 0):
            height, width, channels = self.get_frame().shape
        else:
            width = 0
            height = 0
        self.width = width
        self.height = height

        
    def get_frame(self):#,color):
        response = requests.get(self.video_source)
        img = numpy.array(Image.open(BytesIO(response.content)).convert('RGB'))
        
        return img

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    

def main():

    #btTransmit1 = BT('00:06:66:f2:30:85',1)
    btTransmit1 = BT('98:D3:11:FC:19:4C',1)
    #btTransmit2 = BT('98:D3:11:FC:19:4C',1)
    # Web picture: http://10.161.103.207/html/cam_pic.php
    vs1 = VideoStream2('http://10.161.31.159/html/cam_pic.php')#'http://10.161.103.207/html/cam_pic_new.php')#1)    # Camera 1
    vs2 = VideoStream2(0)    # Camera 2\
    
    
    #img.show()
    
    #vs1.start()
    OD1 = Object_Detection.Obj_Detection(vs1,btTransmit1)
    
    
    root = Tk()
    # MUST BE THE LAST THING THAT HAPPENS
    app = GUI.GUI(btTransmit1,vs1,vs2,OD1)   #btTransmit1
    root.mainloop()
    app.transmit.close() 
    print('Connection closed')
    #vs1.stop()
    
    #GUI.main()


if __name__ == '__main__':
    main()