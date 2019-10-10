


class Experiment(object):
	def __init__(self,id,priority):
		self.priority = priority
		self.id = id
		self.nodes = []
		self.status = ''
		self.duration = 0
		self.protocol = ''
		self.title = ''
		self.nodes = []
		self.scenario = []
		print("[+] New Experiment With ID " + str(self.id))
	def __lt__(self,other):
		return self.priority < other.priority


