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
import signal
import threading

class BT():
    def __init__(self, serverMACAddress = '98:D3:11:FC:19:4C', port=1):
        #serverMACAddress = '98:D3:11:FC:19:4C'
        self.port = port
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Trying to connect')
        self.s.connect((serverMACAddress, port))
        print('Connected')
    def send(self,data,changeData):
        #print('BT SENDING')
        if changeData == 1:
            if data =='a':
                self.s.send('j')
            elif data=='w':
                self.s.send('i')
            elif data=='s':
                self.s.send('k')
            elif data=='d':
                self.s.send('l')
            elif data=='f':
                self.s.send('p')
            elif data=='q':
                self.s.send('o')
            elif data=='x':
                self.s.send('m')
            else:
                self.s.send(data)
        else:
            self.s.send(data)
        #print('BT SENT')
    def close(self):
        self.s.close()

class VideoStream2:
    def __init__(self, video_source=1):
        self.video_source = video_source
        self.prevIMG = 0
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
        #print('LOAD WEB IMAGE')
        try:    
            response = requests.get(self.video_source, timeout = 1)
        except requests.ConnectTimeout:
            print('WEB LOAD ERROR!!! - '+str(self.video_source))
            return self.prevIMG
        except requests.ReadTimeout:
            print('WEB LOAD ERROR!!! - '+str(self.video_source))
            return self.prevIMG
        except requests.ConnectionError:
            print('WEB LOAD ERROR!!! - '+str(self.video_source))
            return self.prevIMG
        #print('WEB IMAGE RECEIVED')
        img = numpy.array(Image.open(BytesIO(response.content)).convert('RGB'))
        #print('CONVERT IMAGE COLOR')
        self.prevIMG = img
        return img



def main():

    
    
    btTransmit1 = BT('00:06:66:F2:30:85',1)
    btTransmit2 = BT('00:06:66:F2:4C:E4',1)
    # Web picture: http://10.161.103.207/html/cam_pic.php
    vs1 = VideoStream2('http://10.161.155.167/html/cam_pic.php')#'http://10.161.103.207/html/cam_pic_new.php')#1)    # Camera 1
    vs2 = VideoStream2('http://10.161.111.139/html/cam_pic.php')    # Camera 2
    
    
    #img.show()
    
    OD1 = Object_Detection.Obj_Detection(vs1,btTransmit1,0)
    OD2 = Object_Detection.Obj_Detection(vs2,btTransmit2,1)
    
    root = Tk()
    # MUST BE THE LAST THING THAT HAPPENS
    app = GUI.GUI(root,btTransmit1,btTransmit2,vs1,vs2,OD1,OD2)   #btTransmit1
    root.mainloop()
    app.transmit1.close() 
    app.transmit2.close() 
    print('Connections closed')


if __name__ == '__main__':
    main()