from NodeManager import NodeManager
import socketserver
import time

import pickle
import signal
import os
import logging
import sys
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import json


def handler(signum = None, frame = None):
    print('Signal handler called with signal', signum)
    manager.close()
    time.sleep(1)  #here check if process is done
    print('Done')
    sys.exit(0)


readings = []

class MyTCPHandler(socketserver.BaseRequestHandler):
    # this method for converting binary to string, packets come from network, also check if there is error
    def node_recv(self):
        try:
            msg = str(self.request.recv(1024),'utf-8')
            if msg == b'':
                print("[-] Connection Broken")
                self.request.close()
            return msg
        except Exception as e:
            print("[-] Could not receive: " + str(e))
            return False
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            msg = self.node_recv()
            command = msg.split("/")
            print(msg)
            if 'quit' in msg:
                self.request.close()
                break
            if 'status' in command[0]:
                if len(command) == 1:
                    status = manager.status
                    output = json.dumps(status)
                    self.request.send(output.encode())
                elif 'zigbee' in command[1]:
                    status = manager.zigbee.prop
                    output = json.dumps(status)
                    self.request.send(output.encode())

            if 'read' in command[0]:
                if 'temp' in command[1]:
                    interval = int(command[2])
                    duration = int(command[3])
                    counter = int(duration/interval)
                    for i in range(counter):
                        output = manager.read_temperature()
                        readings.append(output)
                        output = "temp " + str(output)
                        print("Reading" + output)
                        manager.zigbee.zsend(output)
                        time.sleep(1.5)
                        message = manager.zigbee.get_one_message()
                        message = pickle.dumps(message)
                        #print(message)
                        #message = "Got Packet\n".encode()
                        self.request.send(message)
                        time.sleep(interval)
                    message = "done"
                    message = pickle.dumps(message)
                    self.request.send(message)

                if 'humdity' in command[1]:
                    interval = int(command[2])
                    duration = int(command[3])
                    counter = int(duration/interval)
                    for i in range(counter):
                        output = manager.read_temperature()
                        readings.append(output)
                        output = "Humdity " + str(output)
                        print("Reading" + output)
                        manager.zigbee.zsend(output)
                        time.sleep(1.5)
                        message = manager.zigbee.get_one_message()
                        message = pickle.dumps(message)
                        self.request.send(message)
                        time.sleep(interval)
                    message = "done"
                    message = pickle.dumps(message)
                    self.request.send(message)

            if 'cord' in command[0]:
                #interval = int(command[1])
                #duration = int(command[2])
                #counter = int(duration/interval)
                #for i in range(counter):
                if len(manager.zigbee.messages) == 0:
                    msg = "no msgs\n"
                    msg = pickle.dumps(msg)
                    self.request.send(msg)
                else:
                    length = len(manager.zigbee.messages)
                    msg = str(length) + "\n"
                    msg = pickle.dumps(msg)
                    self.request.send(msg)

            if 'gmsg' in command[0]:
                msg = manager.zigbee.get_one_message()
                msg = pickle.dumps(msg)
                self.request.send(msg)

            if 'zigbee' in command[0]:
                if 'changetocord' in command[1]:
                    if manager.zigbee.cord:
                        msg =  "Already A Cordinator"
                        self.request.send(msg.encode)
                    else:
                        manager.change_Zigbee_cord()
                        msg = "[+] Change To Cordinator"
                        self.request.send(msg.encode)
                elif 'changetoroute' in command[1]:
                    if not manager.zigbee.cord:
                        msg = "Already A Router"
                        self.request.send(msg.encode)
                    else:
                        manager.change_Zigbee_route()
                        msg =  "[+] Change To Router"
                        self.request.send(msg.encode)
                elif 'set' in command[1]:
                    manager.zigbee.set_reciever_address(command[2],command[3])
                    msg = "OK  Address has been set\n"
                    self.request.send(msg.encode())
                elif 'clear' in command[1]:
                    try:
                        manager.zigbee.messages.clear()
                        #self.request.send("Buffer Has been Cleared".encode())
                    except Exception as e:
                        print("error clearing buffer of zigbee " + str(e))


              
            
    def finish(self):
        print("[+] Request Finishes")
        



LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = 'node.log',level = logging.DEBUG,format = LOG_FORMAT)
logger = logging.getLogger()

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, handler) 

name = os.environ['USER']
interface = ni.interfaces()[1]
ipv4_addr =  ni.ifaddresses(interface)[AF_INET][0]['addr']
manager = NodeManager(name)
manager.start()




HOST, PORT = '', 9998
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server.allow_reuse_address = True
print("[+] Start listening")
server.serve_forever()







