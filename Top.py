import GUI
import bluetooth


class BT():
    def __init__(self):
        serverMACAddress = '98:D3:11:FC:19:4C'
        port = 1
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Trying to connect')
        self.s.connect((serverMACAddress, port))
        print('Connected')
    def send(self,data):
        self.s.send(data)
    def close(self):
        self.s.close()


#sock = BT()
def main():

    
    # Other MAC addresses that failed
    #'a0:a8:cd:dc:87:9f' #'F4:37:B7:D2:16:36' '3C:15:C2:BC:DD:A5' '98:D3:11:FC:19:4C' 'E4:F8:9C:33:C9:DE'
    '''
    serverMACAddress = '98:D3:11:FC:19:4C'
    port = 1
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('Trying to connect')
    s.connect((serverMACAddress, port))
    print('Connected')
    
    global s
    serverMACAddress = '98:D3:11:FC:19:4C'
    port = 1
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('Trying to connect')
    s.connect((serverMACAddress, port))
    print('Connected')
    GUI.main()
#    while 1:
        #text = input('Send: ') # Note change to the old (Python 2) raw_input
        #if text == "quit":
        #    break
 #       s.send(GUI.keyHit)
    s.close()
    '''
    GUI.main()


if __name__ == '__main__':
    main()