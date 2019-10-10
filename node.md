
  # Node
  The Node code have 5 .py files, 
  1. run
  2. nodemanager
  3. myzigbee
  4. grovepi
  5. task
  
  run.py, start the code, it include 2 things
  1. socket server
  2. signal handler
  
  The socket server listen for incoming connection , each connection call the handle method , and the node_recv method convert the bytes to string, also check for connection close
  
  self.request represent your connect, with methods like send, recv and close, for more information implement the next example
  
  
  ```python
  import socketserver
  
  class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
      message = str(self.request.recv(1024),'utf-8')
      print(message)
      self.request.send(message.encode())
      # note that 1024 is the max reading bytes, so not nessery to read 1024
      self.request.close()
      
  HOST, PORT = '', 9998
  server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
  server.allow_reuse_address = True
  print("[+] Start listening")
  server.serve_forever()
      
  
  ```
  
  in this example, you will create a echo server ( echo server is a server which reply with the same message you sent) , it listen to port 9998, in all system interface ( so localhost + your home network )
  
  try it out with nc as client, open 2 terminal, one of them in same directory of the example
  
  ##### Terminal 1
  ```bash
  $ python3 ex1_sockserver.py
  ```
  ##### Terminal 2
  ```bash
  ➜  ~ nc localhost 9998
  hi
  hi
  a
  ➜  ~ nc localhost 9998
  aaa
  aaa
  
  ```
  for more information about socketserver check out : [socketserver doc](https://docs.python.org/3/library/socketserver.html)
  
  The other part of run.py, is signal handler, which when you press Ctrl+C it make sure that the program closes peacefully, because sometime you can break zigbee serial connection, and then you will have to take it off, and plug it back in
  
  then when the controller send a command, i execute the function needed.
  
  #### Node Manager
  
  This is the main piece the hold everything togather, the first thing run here is the run method, however you can access everything from outside ( like from run.py file)
  
  so when a task come, there is a thread running the task, but i can access the class variable from run.py ( very bad design because it can break stuff ).
  
  however it's not the complicated, you have a queue inside the class, and there is an endless loop running check if there is a task or not, if there is it execute it, else keep waiting
  
  The other function like close + read_temp + read_humdity are very clear, they do one thing
  
  now if one of the raspberry pi does not have a sensor board, comment out the grovepi library
  
  ```python
  #from grovepi import *
  ```
  
  because python is interpreted language, it's not an error until the method of read_temp be called ( again bad design >.> )
  
  #### Task
   The task file hold a class with couple of attribute, it meant to be a priority queue, not a normal queue, so the idea is if there is a normal task of reading a couple of sensor, it can hold a prioity of something like 5, but if you want to cancel it, you can add a task of priority of 2 or 3 which is lower so it will be executed first
   
   you can think of it, as a normal array but you controll how you place your element by a number called priority ( again i didnt implement this so dont give a shit about the **__lt__** method )
   
   #### myzigbee
   it a class the make zigbee work, if you hate yourself, try to understand it :) ( good luck with that :P :P :P :P :P )
  
'''
tags: []
isStarred: false
isTrashed: false
