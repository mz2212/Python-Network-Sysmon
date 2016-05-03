# Imports
import time
import socket
import psutil
import pickle

# Vars
host = '192.168.11.200'
port = 7166
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
colors = {red, green, blue}
# init doodads
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
	while 1:
		cpuUsage = psutil.cpu_percent(interval = 1)
		data = 'CPU: ' + repr(int(cpuUsage)) + '%'
		if cpuUsage <= 25:
			color = 2
		elif cpuUsage <= 75 and cpuUsage > 25:
			color = 3
		elif cpuUsage < 75:
			color = 1


		sock.sendto(data.encode('utf-8'), (host, port))
		sock.sendto(pickle.dumps(colors[color]), (host, port))
except KeyboardInterrupt:
	print("Ctrl-C Recived, Stopping!")

finally:
	sock.close()
