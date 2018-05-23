import socket
import threading
import sys
import time
import signal
import os
import gzip

class Web(object):

	def __init__(self, port = 4621):
		self.host = "10.89.238.47"
		self.port = port
		self.server_path = '/Users/ivanxivan/Desktop/4621_proj/server'
		self.thread_num = 0

	def shutdown(self):
		try:
			socket.shutdown(SHUT_RDWR)
		except Exception as e:
			pass

	def start(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

		try:
			print("Building server on {h}:{p}".format(h= self.host, p=self.port))
			self.socket.bind((self.host, self.port)) 
			print("Server started at {port}".format(port=self.port))

		except Exception as e:
			print("cannot bind")
			self.shutdown()
			sys.exit(1)

		#Listener
		self.socket.listen(5)
		while True:
			print("accepting the connection")
			self.thread_num = self.thread_num + 1
			(c, addr)= self.socket.accept()
			print("accepted client{x}, {y}".format(x= c, y= addr))
			c.settimeout(60)       
			print ("Got connection from{addr}".format(addr=addr))
		   	t = threading.Thread(target=self.client_handler, args=(c, addr, self.thread_num))
		   	t.start()
	
	#handle the client request and generate the response msg
	def client_handler(self, c, addr, thread_num):


		while True:
			print("start the thread{num}".format(num =thread_num))

			print("self:{s}, client:{c}, address:{addr}".format(s=self, c=c, addr=addr))
			data = c.recv(4096).decode()
			print("Data received for thread{num}:\n {d}".format(num=thread_num, d=data))

			#start handle the data
			method = data.split(' ')[0]
			print("method: {m}".format(m = method))

			if method == "GET":
				request_file = data.split(' ')[1]

				if request_file == "/":
					request_file = "/index.html"

				print("request_file: {f}".format(f = request_file))
				file_path = self.server_path  + request_file

				type_of_file = request_file.split('.')[1]
				print("type of file: {t}".format(t = type_of_file))

				print("server_file_path: {sfp}".format(sfp = file_path))


				try:
					time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

					file = open(file_path, 'r')
					response_file = file.read()
					file.close()
					response_file = gzip.Gzipfile(fileobj=response_file)
					response_msg = ' '
					response_msg += 'HTTP/1.1 200 OK\r\n'
					response_msg += 'Date: {time}\r\n'.format(time = time_now)
					response_msg += 'Accept-Ranges: bytes\r\n'

					# if type_of_file == "html":
					# 	response_msg += 'Content-Type: {type}\n\n'.format(type = 'text/html')
					if type_of_file == "jpg":
						response_msg += 'Content-Type: {type}\r\n'.format(type = 'image/jpeg')
					elif type_of_file == "pdf":
						response_msg += 'Content-Type: {type}\r\n'.format(type = 'application/pdf')
					elif type_of_file == "pptx":
						response_msg += 'Content-Type: {type}\r\n'.format(type = 'application/ppt')
					else:
						response_msg += 'Content-Type: {type}\r\n'.format(type = 'text/html')

					statinfo = os.stat(file_path)
					size = statinfo.st_size
					print("size: {s}".format(s=size))
					response_msg += 'Content-Length: {length}\r\n'.format(length=size)

					#response_msg += 'Content-Encoding: gzip\r\n'

					response_msg += 'Connection: Keep-Alive\r\n'

					response_msg += 'Server: 4621_proj_server\n\n'

					response_msg += response_file

				except Exception as e :
					file_path = self.server_path  + "/404.html"
					file = open(file_path, 'r')
					response_file = file.read()
					file.close()
					 
					response_msg = 'HTTP/1.1 404 Not Found\r\n'
					response_msg += 'Date: {time}\r\n Server: 4621_proj_server\n\n'.format(time = time_now)
					response_msg += response_file

					response_msg.encode()

				c.send(response_msg)
				print("response_msg: \n {d}".format(d=response_msg))
				print("end of thread{num}".format(num=thread_num))
				c.close()
				break



