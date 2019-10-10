import json
import socket
import threading
import queue
import pickle
import time
import csv
import shutil
from Task import Task
from databaseConnection import DatabaseConnection


class Node(threading.Thread):
    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.name = ""
        self.ipv4 = ip
        self.port = port
        self.socket = None
        self.available = False
        self.zigbee = False
        self.zigbee_properties = None
        self.zigbee_addr_long = ''
        self.zigbee_addr_short = ''
        self.zigbee_cordy = False
        self.lowpan = False
        self.sensorTemp = False
        self.sensorHumdity = False
        self.status = {}
        self.daemon = True
        self.running = True
        self.queue = queue.PriorityQueue()
        self.pid = 0
        self.eid = 0
        self.packets_indicator = []
        self.get_indi = False
        self.get_packs = False
        self.keep_running = True
        self.reciver_addr_long = ''
        self.reciver_addr_short = ''
        self.temp_interval = 0
        self.humdity_interval = 0
        self.duration = 0
        self.counter = 0
        self.sender_name = ''
        self.db = DatabaseConnection()


        
    def node_recv_str(self):
        if self.available:
            try:
                msg = str(self.socket.recv(1024),'utf-8')
                if msg == b'':
                    print("[-] Connection Broken")
                    self.socket.close()
                return msg
            except Exception as e:
                print("[-] Could not receive: " + str(e))
                return False

    def node_recv_bytes(self):
        if self.available:
            try:
                msg = self.socket.recv(1024)
                if msg == b'':
                    print("[-] Connection Broken")
                    self.socket.close()
                return msg
            except Exception as e:
                print("[-] Could not receive: " + str(e))
                return False

    def node_send_str(self,msg):
        if self.available:
            try:
                self.socket.send(msg.encode())
                return True
            except Exception as e:
                print("[-] Could not send: " + str(e))
                self.close_socket()
                return False
        
    def extract(self,data):
        self.name = data['name']
        self.zigbee = data['zigbee']
        self.lowpan = data['lowpan']
        self.sensorTemp = data['Temperature']
        self.sensorHumdity = data['Humdity']
        self.status = {"name":self.name,
                        "zigbee":self.zigbee,
                        "lowpan":self.lowpan,
                        "Temperature":self.sensorTemp,
                        "Humdity":self.sensorHumdity}
                        
    
    def run(self):
        self.connect()
        self.collect_status()
        self.close_socket()
        self.main_loop()  
        


    def main_loop(self):
        while self.keep_running:
            if self.get_indi:
                self.clear_buffer()
                self.connect()
                self.get_indicator()
                self.close_socket()
            elif self.get_packs:
                self.connect()
                self.get_packets()
                self.close_socket()
            time.sleep(1)

    def assign_counter_message(self):
        self.node_send_str("cord")
        msg = self.socket.recv(1024)
        msg = pickle.loads(msg)
        if 'no msgs' in msg:
            self.counter = 0
        else:
            self.counter = int(msg)

    def clear_buffer(self):
        self.connect()
        self.node_send_str("zigbee/clear")
        self.packets_indicator.clear()
        self.close_socket()

    def get_packets(self):
        self.assign_counter_message()
        print("Packets: " + str(self.counter))
        for i in range(self.counter):
            self.node_send_str('gmsg')
            msg = self.socket.recv(1024)
            msg = pickle.loads(msg)
            print(msg)
            self.packets_indicator.append(msg)
            time.sleep(1)
        path = self.write_to_csvPackets()
        self.save_res(path)
        self.get_packs = False

    def save_res(self,path):
        folder_name = "results"
        output =  folder_name + "/" + path
        self.db.save_results(self.pid,self.eid,output)
        results_folder = "/home/aziz/interface/results/"
        shutil.move(path,results_folder)

    def read_temp(self):
        if self.available:
            if self.sensorTemp:
                if self.node_send_str("read/temp"):
                    read = self.node_recv_str()
                    print(read)



    def get_indicator(self):
        self.set_address_in_node()
        self.read_temp()
        self.read_humdity()
        self.get_indi = False
        path = self.write_to_csvIdicator()
        self.save_res(path)


        
    def read_temp(self):
        if self.temp_interval == 0:
            return
        tempcounter = int(self.duration/self.temp_interval)
        temp_read = 'read/temp/' + str(self.temp_interval) + "/" + str(self.duration)
        self.socket.send(temp_read.encode())
        while True:
            msg = self.socket.recv(1024)
            msg = pickle.loads(msg)
            print(msg)
            if 'done' in msg:
                print("done")
                break
            else:
                self.packets_indicator.append(msg)
            time.sleep(1)

    def read_humdity(self):
        if self.humdity_interval == 0:
            return
        humdityCounter = int(self.duration/self.humdity_interval)
        humdity_read = 'read/humdity/' + str(self.humdity_interval) + "/" + str(self.duration)
        self.socket.send(humdity_read.encode())
        while True:
            msg = self.socket.recv(1024)
            msg = pickle.loads(msg)
            print(msg)
            if 'done' in msg:
                print("done")
                break
            else:
                self.packets_indicator.append(msg)
            time.sleep(1)

    def change_Zigbee_cord(self):
        if self.available:
            if self.zigbee:
                if self.zigbee_cordy:
                    print("Already Cordinator")
                else:
                    if self.node_send_str("zigbee/changetocord"):
                        self.node_recv_str()
                        time.sleep(30)
                        self.collect_zigbee()
            else:
                print("No Zigbee")
    def change_Zigbee_route(self):
        if self.available:
            if self.zigbee:
                if not self.zigbee_cordy:
                    print("Already Router")
                else:
                    if self.node_send_str("zigbee/changetoroute"):
                        response = self.node_recv_str()
                        print(response)
                        time.sleep(30)
                        self.collect_zigbee()
            else:
                print("No Zigbee")


    def send_task(self):
        pass
                    
    def collect_status(self):
        if self.available:
            if self.node_send_str("status"):
                data = self.node_recv_str()
                print(data)
                self.extract(json.loads(data))
                self.collect_zigbee()
                
    def collect_zigbee(self):
        if self.zigbee:
            if self.node_send_str("status/zigbee"):
                zigbee_info = self.node_recv_str()
                self.extract_zigbee(json.loads(zigbee_info))
                print("zigbee: "  + str(self.zigbee_properties))

    def assign_zigbee_address(self,long_addr,short_addr):
        self.reciver_addr_long = long_addr
        self.reciver_addr_short = short_addr

    def set_address_in_node(self):
        cord_address = 'zigbee/set/'+ str(self.reciver_addr_long) + '/' + str(self.reciver_addr_short)
        self.socket.send(cord_address.encode())
        msg = self.node_recv_str()
        if 'OK  Address has been set' in msg:
            return True
        else:
            return False
    
    def close_socket(self):
        self.running = False
        self.socket.send("quit".encode())
        self.socket.close()
        
    def connect(self):
        self.socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[+] Connecting: " + str(self.ipv4) + " : " + str(self.port))
        try:
            self.socket.connect((self.ipv4,self.port))
            self.available = True
        except Exception as e:
            print("[-] Could not Connect To: " + str(self.ipv4) +" Because: " + str(e))
            self.available = False
            self.status = {"ip":self.ipv4,
                            "available":"no"}
            
    def extract_zigbee(self,data):
        self.zigbee_properties = data
        if self.zigbee_properties['CE'] == '1':
            self.zigbee_cordy = True
        else:
            self.zigbee_cordy = False
        self.zigbee_addr_long = "00" + self.zigbee_properties['SH'] + self.zigbee_properties['SL']
        if len(self.zigbee_properties['MY']) == 3:
            self.zigbee_addr_short = "0" + self.zigbee_properties['MY']
        else:
            self.zigbee_addr_short =  self.zigbee_properties['MY']
        
    def add_task(self,Task):
        self.queue.put(Task)


    def get_task(self):
        return self.queue.get()

    def write_to_csvIdicator(self):
        name = self.name + "-" + str(self.eid)+"-" + str(self.pid)
        path = name + ".csv"
        file = open(path,'w')
        writer = csv.writer(file)
        writer.writerow(["id","retries","discover_status","frame_id","dest_addr","deliver_status"])
        for data in self.packets_indicator:
            i_id = data['id']
            retries = data['retries']
            discover_status = data['discover_status']
            frame_id = data['frame_id']
            dest_addr = data['dest_addr']
            deliver_status = data['deliver_status']
            writer.writerow([i_id,retries,discover_status,frame_id,dest_addr,deliver_status])
        file.close()
        return path

    def write_to_csvPackets(self):
        name = self.name + "-" + str(self.eid)+"-" + str(self.pid)
        path = name + ".csv"
        file = open(path,'w')
        writer = csv.writer(file)
        writer.writerow(["sender_name","sensor","read","id","source_addr","dest_endpoint","source_endpoint","cluster","profile","options","source_addr_long"])
        for data in self.packets_indicator:
            i_id = data['id']
            rf_data = str(data['rf_data'],'utf-8')
            sensor,read = rf_data.split(' ')
            source_addr = data['source_addr']
            dest_endpoint = data['dest_endpoint']
            source_endpoint = data['source_endpoint']
            cluster = data['cluster']
            profile = data['profile']
            options = data['options']
            source_addr_long = data['source_addr_long']
            writer.writerow([self.sender_name,sensor,read,i_id,source_addr,dest_endpoint,source_endpoint,cluster,profile,options,source_addr_long])
        file.close()
        return path



    def __str__(self):
        if self.zigbee:
            return  "Name: " + self.name +"\nIpv4: " + self.ipv4 +"\nZigBeeSupport: " \
                + str(self.zigbee) + "\n6lowPanSupport: " + str(self.lowpan)  +"\nAvailable: "\
                 + str(self.available) + "\nZigbeeLongAddr: " + str(self.zigbee_addr_long) + "\nZigbeeShortAddr: " + str(self.zigbee_addr_short) + "\n"
        else:
            return  "Name: " + self.name +"\nIpv4: " + self.ipv4 +"\nZigBeeSupport: " \
                + str(self.zigbee) + "\n6lowPanSupport: " + str(self.lowpan)  +"\nAvailable: "\
                 + str(self.available) + "\n"
        
