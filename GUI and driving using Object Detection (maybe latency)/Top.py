import GUI
import Object_Detection
import bluetooth
import imutils
from imutils.video import VideoStream
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from tkinter import font
from PIL import Image
from PIL import ImageTk
from tkinter import *
import time


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
        # Open the video source
        print('Loading video feed')
        self.vid = cv2.VideoCapture(video_source)
        print('VideoCapture done')
      #  self.vidSt = VideoStream(src=video_source).start()
      #  print('VideoStream done')
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        time.sleep(2.0)
 
    def get_frame(self,color):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                if(color>0):
                # Return a boolean success flag and the current frame converted to BGR
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)
 
   # def get_frame2(self):
   #     print('reading')
   #     return self.vidSt.read()
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    

def main():

    btTransmit1 = BT('98:D3:11:FC:19:4C',1)
    #btTransmit2 = BT('98:D3:11:FC:19:4C',1)
    vs1 = VideoStream2('http://admin:admin@10.161.74.194:8081')#1)    # Camera 1
    vs2 = VideoStream2(0)    # Camera 2
    
    OD1 = Object_Detection.Obj_Detection(vs1,btTransmit1)
    
    
    root = Tk()    
    # MUST BE THE LAST THING THAT HAPPENS
    app = GUI.GUI(btTransmit1,vs1,vs2,OD1)   #btTransmit1
    root.mainloop()
    app.transmit.close() 
    print('Connection closed')
    
    #GUI.main()


if __name__ == '__main__':
    main()