import threading


class mockThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		for i in range(5):
			print(i)




thread1 = mockThread()
for i in range(6,10):
	print(i)

thread1.start()
#thread1.join()