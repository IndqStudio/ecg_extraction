# Importing Libraries
import serial  #pip install pyserial
import time
import keyboard  #pip install keyboard

class arduino_pyserial:
    def __init__(self,COM,BAUD=115200,TIMEOUT=.1):
        self.COM=COM
        self.BAUD=BAUD#baudrate default 115200
        self.TIMEOUT=TIMEOUT
        self.arduino=''
    def init_arduino(self):
         try:
              self.arduino=serial.Serial(port=self.COM, baudrate=self.BAUD, 
                                         timeout=self.TIMEOUT)      
         except Exception as e :
              print("port busy, restart")
    def read_data(self):
        try:
            data=self.arduino.readline()
            return data
        except Exception as e :
            return e
        
    def close_com(self):
        print("closing com "+self.COM)
        self.arduino.close()
        return 
    
ar=arduino_pyserial("COM4") 
ar.init_arduino()#init arduino port ,might cause erro if port is not closed.Replug the board 
lead1=[]
lead2=[]
lead3=[]
try:
    while (keyboard.is_pressed('q')==False):
            dat=str(ar.read_data()).strip("b'\\r\\n' ").split(',')
            lead1.append(int(dat[0]))
            lead2.append(int(dat[1]))
            lead3.append(int(dat[2]))   
    ar.close_com()
except :
        ar.close_com()
      