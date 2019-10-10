
class Task(object):
    def __init__(self):
        self.priority = 4
        self.id = 0
        self.command = ''
        self.interval = 0
        self.duration = 0
        self.counter = 0
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    def __lt__(self,other):
    	return self.priority < other.priority
