# Importing Libraries
# from turtle import color
import serial  #pip install pyserial
import time
import keyboard  #pip install keyboard
import pandas as pd 
import datetime   
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

#use below line for jupyter notebook for display 
#----------------------
#%matplotlib notebook
#----------------------
plt.ion()



class DynamicUpdate():
    #Suppose we know the x range
    # def center(self, data)

    def on_launch(self):
        #Set up plot
        
        self.figure, self.ax = plt.subplots(3,1, figsize=(35,15))
        # self.figure.set_figheight(15)
        # self.figure.set_figwidth(25)

        self.lines1, = self.ax[0].plot([],[], 'g')
        self.lines2, = self.ax[1].plot([],[], 'g')
        self.lines3, = self.ax[2].plot([],[], 'g')
        self.ax[0].set_facecolor("black")
        self.ax[1].set_facecolor("black")
        self.ax[2].set_facecolor("black")
        self.ax[0].set_ylabel("channel-1")
        self.ax[1].set_ylabel("channel-2")
        self.ax[2].set_ylabel("channel-3")



        #Autoscale on unknown axis and known lims on the other
        self.ax[0].set_autoscaley_on(True)
        self.ax[1].set_autoscaley_on(True)
        self.ax[2].set_autoscaley_on(True)


        #Other stuff
        # self.ax[0].grid(color='green')
        # self.ax[1].grid(color='green')
        # self.ax[2].grid(color='green')



    def on_running(self, time, ch1, ch2, ch3):
        #Update data (with the new _and_ the old points)
        self.lines1.set_xdata(time)
        self.lines1.set_ydata(ch1)
        self.lines2.set_xdata(time)
        self.lines2.set_ydata(ch2)
        self.lines3.set_xdata(time)
        self.lines3.set_ydata(ch3)
        
        # self.lines1, = self.ax[0].plot(time,ch1, 'r')
        # self.lines2, = self.ax[1].plot(time,ch2, 'g')

        # self.ax.set_autoscaley_on(True)


        #Need both of these in order to rescale
        self.ax[0].relim()
        self.ax[1].relim()
        self.ax[2].relim()


        self.ax[0].autoscale_view()
        self.ax[1].autoscale_view()
        self.ax[2].autoscale_view()


        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

class arduino_pyserial:
    def __init__(self,COM,BAUD=57600,TIMEOUT=.01):
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


    
def save_file(l1,l2,l3,t):
        dict  = {"time":t,'lead1': l1, 'lead2':l2 , 'lead3': l3}
        df=pd.DataFrame(dict) 
        timestamp= datetime.datetime.now().timestamp()
        file_name=str(timestamp)+".csv"
        
        if os.path.exists("ECG_CSV"):
            df.to_csv('ECG_CSV/'+file_name) 
        else:
            os.mkdir("ECG_CSV")
            df.to_csv('ECG_CSV/'+file_name) 
        print("file saved as:"+file_name)
        return
    
    

    
ar=arduino_pyserial("/dev/ttyACM0") 
dy_plot = DynamicUpdate()
dy_plot.on_launch()
ar.init_arduino()#init arduino port ,might cause erro if port is not closed.Replug the board 
lead1=[]
lead2=[]
lead3=[]
time=[]
index=[]#temp for plotting 

def center(x):
    mean = np.mean(x, axis=0, keepdims=True)
    centered =  x - mean
    return centered

# b, a = scipy.signal.butter(3, [0.05, .1], 'band')
b, a = scipy.signal.butter(3, 0.05, 'highpass')

# f6 = scipy.signal.lfilter(b, a, data8.iloc[500:,0])
try:
    print('data reading started press q to stop')
    while (keyboard.is_pressed('q')==False):# press keyboard q to stop the loop
            dat=str(ar.read_data()).strip("b'\\r\\n' ").split(',')#clean the string coming in byte format
            print(dat,"end...")
            if(len(dat)<3):
                dat = ['0','0','0']
            if(str.isdigit(dat[0])==False or str.isdigit(dat[1])==False or str.isdigit(dat[2])==False):
                dat = ['0','0','0']
            
            # print(dat)
            lead1.append(int(dat[0]))
            lead2.append(int(dat[1]))
            lead3.append(int(dat[2]))
            time.append(datetime.datetime.now())
            index.append(len(lead1))
            center_filter1 = scipy.signal.lfilter(b,a,center(lead1[-180:]))
            center_filter2 = scipy.signal.lfilter(b,a,center(lead2[-180:]))
            center_filter3 = scipy.signal.lfilter(b,a,center(lead3[-180:]))
            # print(center_filter1, len(center_filter1),"bef0re")

            # if(center_filter1[len(center_filter1)-1]<-200000):
            #     lead1[len(lead1)-1]=0
            #     center_filter1[len(center_filter1)-1]=0
            # diff = lead1[len(lead1)-1] - lead1[len(lead1)-2]
            # if(diff<-200000):
            #     lead1[len(lead1)-1]=0

            # print(center_filter1[len(center_filter1)-1],len(center_filter1)-1)
            # print(center_filter1, len(center_filter1),"after")
            # print(len(lead1), len(center_filter1))
            print(len(lead1))
            # np.linspace(0,len(lead1)/2, num=len(lead1))
            dy_plot.on_running(index[-150:],center_filter1[-150:],center_filter2[-150:], center_filter3[-150:])#sending last 10 points to plot 

          
            
    ar.close_com()
    # save_file(lead1,lead2,lead3,time)#saving file after "q" is pressed otherwise won't 
  
except Exception as e :
        print(e)
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
