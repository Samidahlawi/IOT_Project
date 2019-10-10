import threading
import queue
import time
from myzigbee import myZigbee
import logging
from Tasks import Task
#from grovepi import *

class NodeManager(threading.Thread):
	def __init__(self,name):
		threading.Thread.__init__(self)
		self.counter = 0
		self.workers = []
		self.name = name
		self.daemon = True
		self.running = True
		self.queue = queue.PriorityQueue()
		self.zigbee = myZigbee()
		if self.zigbee:
			self.supportZigbee = True
		else:
			self.supportZigbee = False
		self.supportLowpan = False
		self.sensorTemp = False
		self.sensorHumdity = False
		self.status = {"name":self.name,
						"zigbee":self.supportZigbee,
						"lowpan":self.supportLowpan,
						"Temperature":self.sensorTemp,
						"Humdity":self.sensorHumdity}
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
		logging.basicConfig(filename = 'nodeManager.log',level = logging.DEBUG,format = LOG_FORMAT)
		self.logger = logging.getLogger()
		self.tasks = []
		self.zigbee.printProperties()


	def run(self):
		print("[+] Manager Started")
		self.logger.info("Manager Started")
		while self.running:
			task = self.get_task()
			task.status = "Running"
			print("Doing: " + str(task.command) )
			if 'close' in  task.command:
				self.close
			task.status = "Done"
			self.tasks.append(task)
			time.sleep(1)

	def close(self):
		self.zigbee.close_port()
		self.running = False

	def add_task(self,id,command):
		print("[+] Task has been added")
		self.logger.info("[+] Task has been added")
		self.queue.put(Task(id,command))


		## ignore this
		'''
	def parse_command(self,command):
		if 'zigbee' in command[0]:
			if 'changetocord' in command[1]:
				if self.zigbee.cord:
					return "Already A Cordinator"
				else:
					self.change_Zigbee_cord()
					return "[+] Change To Cordinator"
			elif 'changetoroute' in command[1]:
				if not self.zigbee.cord:
					return "Already A Router"
				else:
					self.change_Zigbee_route()
					return "[+] Change To Router"
			elif 'set' in command[1]:
				self.zigbee.set_reciever_address(command[2],command[3])
				return "OK  Address has been set\n"
				'''

	def read_temp_multi(self,interval,duration):
		counter = int(duration/interval)
		print(counter)
		reading = []
		for i in range(counter):
			output = self.read_temperature()
			reading.append(output)
			time.sleep(interval)
		return reading

	def read_humdity_multi(self,interval,duration):
		counter = duration/interval
		reading = []
		for i in range(counter):
			output = self.read_humdity()
			reading.append(output)
			time.sleep(interval)
		return reading

	def change_Zigbee_cord(self):
		self.zigbee.change_to_cord()

	def change_Zigbee_route(self):
		self.zigbee.change_to_route()


	def read_temperature(self):
		[temp,hum] = dht(4,0)
		return temp

	def read_humdity(self):
		[temp,hum] = dht(4,0)
		return hum

	def read_temp_humdity(self):
		[temp,hum] = dht(4,0)
		return [temp,hum]

	def zigbee_send(self,long_addr,short_addr,message):
		self.zigbee.zsend(long_addr,short_addr,message)
		time.sleep(1.5)
		indicator = self.zigbee.get_one_message()
		return indicator

	def lowpan_send(self):
		pass

	def zigbee_recv(self):
		packet = None
		if len(self.zigbee.message) > 0:
			packet = self.zigbee.get_one_message()
		return packet

	def lowpan_recv(self):
		pass


	def get_task(self):
		return self.queue.get() 
