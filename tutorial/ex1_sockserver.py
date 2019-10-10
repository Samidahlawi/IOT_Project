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
