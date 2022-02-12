class serial_read:
    def __init__(self,COM,BAUD=115200,TIMEOUT=.1):
        self.COM=COM
        self.BAUD=BAUD#baudrate default 115200
        self.TIMEOUT=TIMEOUT
        self.arduino=''

    def init_arduino(self):
        #init listening to com port 
         try:
              self.arduino=serial.Serial(port=self.COM, baudrate=self.BAUD,timeout=self.TIMEOUT)      
         except Exception as e :
              print("port busy, restart")
            
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
