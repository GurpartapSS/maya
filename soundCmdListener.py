import socket
import actuatorControl



class localListener:
  def __init__(self):
      self.s = socket.socket()        
      print ("Socket successfully created")
    
      port = 12345               
    
      self.s.bind(('', port))        
      print ("socket binded to %s" %(port))

      self.act = actuatorControl.actuator()
      self.act.setup_gpio()
      print("got actuators connected")

  def Listen(self):
        self.s.listen()    
        print ("socket is listening")

        # Establish connection with client.
        self.c, self.addr = self.s.accept()
        print ('Got connection from', self.addr)
        while True:
              data = self.c.recv(1024)
              if data:
                  data = data.decode('utf-8')
                  print('Received data: ',data)
                  if(int(data) <= 10):
                        self.act.movement_auto(1)
                  if(int(data) == 12):
                        self.act.movement_stop()

if __name__ == "__main__":
  l = localListener()
  l.Listen()