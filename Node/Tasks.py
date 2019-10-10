


class Task(object):
	def __init__(self,id,command,interval,duration):
		self.priority = 4
		self.id = id
		self.command = command
		self.result = []
		self.status = ''
		self.interval = interval
		self.duration = duration
		self.counter = 0

	def __lt__(self,other):
		return self.priority < other.priority



