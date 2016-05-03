# Imports
import time
import socket
import psutil

# Vars
host = '192.168.11.200'
port = 7166

# init doodads
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
	while 1:
		data = 'CPU: ' + repr(int(psutil.cpu_percent(interval = 1))) + '%'

		sock.sendto(data.encode('utf-8'), (host, port))
except KeyboardInterrupt:
	print("Ctrl-C Recived, Stopping!")
	
finally:
	sock.close()
	
	
	
