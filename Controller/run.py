import json
import socketserver
import pickle
#from Node import Node
from ControllerManager import ControllerManager





''''
# this function try to connect to all nodes, and check which one is available and which one is not, then it will print the details for each one.
def bootup():
    for i in Nodes:
        a = Node(i[0],i[1])
        a.connect()
        a.run()
        a.close_socket()
        print(a)
        pNodes.append(a)
'''    
        
def bootup_thread():
    name = "Node 1"
    node = Worker(1, name,"127.0.0.1",9998)
    node.add_job(2,"hi im a job")
    node.start()
    pNodes.append(node)


class MyTCPHandler(socketserver.BaseRequestHandler):

    # this method for converting binary to string, packets come from network, also check if there is error
    def controller_recv(self):
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

            msg = self.controller_recv()
            print("msg: " + msg)
            command = msg.split("/")
            
            if 'close' in msg:
                manager.close()
                self.request.close()
                break
            if 'status' in command[0]:
                if 'number' in command[1]:
                    node_counter = str(len(manager.Nodes))
                    #node_counter = pickle.dumps(node_counter)
                    self.request.send(node_counter.encode())
                if 'id' in command[1]:
                    number = int(command[2])
                    output = manager.Nodes[number].status
                    print(output)
                    output = pickle.dumps(output)
                    #output += "\n"
                    self.request.send(output)
                    #for i in manager.Nodes:
                    #    if "ok" in self.no
                    #    print("sending status")
                    #    output = i.status
                    #    output = pickle.dumps(output)
                        #output += "\n"
                    #    self.request.send(output)
            if 'add' in command[0]:
                number = int(command[1])
                print("Adding Experiment with id: " + str(number))
                manager.add_Experiment(number)
            '''
            if 'status' in command[0]:
                for i in pNodes:
                    output = i.status
                    output = json.dumps(output)
                    self.request.send(output.encode())
            if 'add' in command[0]:
                for i in pNodes:
                    i.add_job(2,"hi im a job")

            else:
                continue
            '''
    def finish(self):
        print("[+] Request Finishes")





Nodes = [("127.0.0.1",9998)
        ,('192.168.1.209',9998)
        ,('192.168.1.208',9998)]


pNodes = []
host = '0.0.0.0'
port = 9999
manager = ControllerManager()
#manager.add_Experiment(1,2)
manager.start()
#connected_nodes = create_sockets(Nodes)

#print("Bootup")
#bootup_thread()
#print("printing nodes")
#check_node()

HOST, PORT = '', 9999

server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server.allow_reuse_address = True
print("[+] Start listening")
server.serve_forever()

