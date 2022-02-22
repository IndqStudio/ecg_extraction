import socket
# // windows first type ipconfig,
# // then check  IPv4 Address starting with ex: 192.168.38.1, 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((socket.gethostname(), 1234))
except:
    s.close()
    #restart the script

s.listen(5)
print(s)
while True:
    # now our endpoint knows about the OTHER endpoint.
    client, address = s.accept()
    content = client.recv(32)
    if len(content) ==0:
           break
    else:
            print(content)
'''
  //esp32 side code 
#include <WiFi.h>

// Replace with your network credentials (STATION)
const char* ssid = "your_wifi_name";
const char* password = "your_password";

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  initWiFi();
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
}
void dummy_data(){
  
  client.write("hello there");
  
  
  
  }
void loop() {
   Serial.print("WiFi connected with IP: ");
    WiFiClient client;
   

     if (! client.connect("192.168.137.1", 1234)) {  
     // windows first type ipconfig,
     // then check  IPv4 Address
 
        Serial.println("Connection to host failed");
 
        delay(1000);
        return;
    }
    else{
      
      client.write("hello there");
      }
    
  Serial.println(WiFi.localIP());
  // put your main code here, to run repeatedly:
}
  '''  
