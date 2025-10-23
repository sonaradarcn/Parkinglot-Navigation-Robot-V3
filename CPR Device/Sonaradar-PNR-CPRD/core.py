from function import *
from socketClient import *
from utils import *
import time
from webUI import *
    


configUtil = ConfigUtil()

def startUP():
    SocketClientCommand.start_socket(server_ip=configUtil.read('server','ip'))
    
SocketClientCommand.start_socket(server_ip=configUtil.read('server','ip'))
bottle_app = BottleApp()
bottle_app.run(host='localhost', port=8080)
while(True):
    time.sleep(1)