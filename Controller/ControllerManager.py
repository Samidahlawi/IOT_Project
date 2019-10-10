import threading
import queue
from Experiment import Experiment
from NodeThread import Node
import time
from databaseConnection import DatabaseConnection
from Task import Task



class ControllerManager(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.queue = queue.PriorityQueue()
		self.nodes_info = [('192.168.1.209',9998),('192.168.1.208',9998),('192.168.1.207',9998)]
		self.Nodes = []
		self.running = True
		self.experiment = None
		self.db = DatabaseConnection()
		self.cordy = None
		self.setup_node()

	def setup_node(self):
		for i in self.nodes_info:
			node = Node(i[0],i[1])
			node.start()
			self.Nodes.append(node)

	def set_cordy(self):
		for i in self.Nodes:
			if i.zigbee_cordy:
				self.cordy = i
	def run(self):
		time.sleep(5)
		self.set_cordy()
		print("[+] ControllerManager Started")
		while self.running:
			self.experiment = self.get_Experiment()
			exp_info = self.db.get_Experiment_info(self.experiment.id)
			if(exp_info['status'] == 'done'):
				print("Experiment Already Done")
				continue
			self.db.change_to_running(self.experiment.id)
			self.experiment.duration = int(exp_info['duration'])
			self.experiment.protocol = exp_info['protocol']
			self.experiment.title = exp_info['title']
			print(self.experiment.title)
			print(self.experiment.protocol)
			print(self.experiment.duration)
			self.experiment.nodes = self.db.get_Node_info(self.experiment.id)
			self.experiment.scenario = self.db.get_scenario_info(self.experiment.id)
			#print(self.experiment.nodes)
			#print(self.experiment.scenario)
			#print(exp_info)
			#self.setup_experiment()
			self.sensor()
			self.read_start()
			self.db.change_to_done(self.experiment.id)


	def setup_experiment(self):
		for node in self.experiment.nodes:
			for i in self.Nodes:
				if node['name'] == i.name:
					if node['protocol'] == 'cord' and i.zigbee_cordy:
						print( i.name +": is coordinator")
					elif node['protocol'] == 'cord' and not i.zigbee_cordy:
						i.change_Zigbee_cord()
					elif node['protocol'] == 'router' and i.zigbee_cordy:
						i.change_Zigbee_route()
					else:
						print( i.name +": is router")
				
				
	def read_start(self):
		print(self.experiment.scenario)
		for path in self.experiment.scenario:
			node1 = None
			node2 = None
			node1_id = path['en1']
			node2_id = path['en2']
			pathId = path['pid']
			print("Node1 ID : " + str(node1_id))
			print("Node2 ID : " + str(node2_id))
			node1_name = self.db.get_node_name(node1_id)
			node2_name = self.db.get_node_name(node2_id)
			print("node1 name " + str(node1_name))
			print("node2 name " + str(node2_name))
			for node in self.Nodes:
				if node.name == node1_name:
					node1 = node
					print(node1)
				if node.name == node2_name:
					node2 = node
					print(node2)
			if node2:
				long_addr = node2.zigbee_addr_long
				short_addr = node2.zigbee_addr_short
				if node1:
					node1.assign_zigbee_address(long_addr,short_addr)
					node1.pid = pathId
					node1.eid = self.experiment.id
					node2.clear_buffer()
					node1.get_indi = True
					while node1.get_indi:
						time.sleep(1)
					node2.pid = pathId
					node2.eid = self.experiment.id
					node2.sender_name = node1_name
					node2.get_packs = True
					while node2.get_packs:
						time.sleep(1)

			else:
				print('node2 not found')

		
	def sensor(self):
		for node in self.experiment.nodes:
			node_name = node['name']
			print("Node: " +node['name'] + " Temp:" + str(node['temperature']) +" Humdiry " + str(node['humdity']))
			for anode in self.Nodes:
				if anode.name == node_name:
					bnode = anode
					print(bnode)
					bnode.temp_interval = int(node['temperature'])
					bnode.humdity_interval = int(node['humdity'])
					bnode.duration = int(self.experiment.duration)

	def add_Experiment(self,id,priority=1):
		self.queue.put(Experiment(id,priority))
		

	def parse(self):
		pass
    
	def get_Experiment(self):
		return self.queue.get()

	def close(self):
		self.running = False
