import socket
# // windows first type ipconfig,
# // then check  IPv4 Address starting with ex: 192.168.38.1, 

class esp32_wifi:
    def __init__(self,port,hostName=socket.gethostname()):
        self.hostName=hostName
        self.port=port
        self.client=''
        self.address=''
        self.content=''
        self.message="init"
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
        return
        
    def bind_port(self):
        self.socket.bind((self.hostName, self.port))
        self.socket.listen(5)
        print("waiting for data")
        self.client, self.address = self.socket.accept()
        return
    
    def unbind_port(self):
        self.socket.close()
        
    def data_read(self):
        self.content = self.client.recv(32)
        return self.content
    
    def data_send(self):
        self.client.sendall('init'.encode())
     
        
        
        
    
       