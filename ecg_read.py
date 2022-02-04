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
        
        #init listening to com port 
         try:
              self.arduino=serial.Serial(port=self.COM, baudrate=self.BAUD, 
                                         timeout=self.TIMEOUT)      
         except Exception as e :
              print(e)
                
    def read_data(self):
        
        #readlines on python side 
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
    while (keyboard.is_pressed('q')==False):# press keyboard q to stop the loop
        
            dat=str(ar.read_data()).strip("b'\\r\\n' ").split(',')#clean the string coming in byte format
            
            lead1.append(int(dat[0]))
            lead2.append(int(dat[1]))
            lead3.append(int(dat[2]))   
    ar.close_com()
except :
        ar.close_com()
      
'''

//arduino side sample code 
void setup() {

  Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
 long  int t =20000000;
  // print out the value you read:
  Serial.print(t,DEC);
   Serial.print(",");
  Serial.print(t,DEC);
   Serial.print(",");
   Serial.print(t,DEC);
   
   Serial.println(" ");
  delay(100);        // delay in between reads for stability
}

'''
