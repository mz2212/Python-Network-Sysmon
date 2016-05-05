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
yellow = (1, 1, 0)
magenta = (1, 0, 1)
cyan = (0, 1, 1)
white = (1, 1, 1)
off = (0, 0, 0)
disk1 = 'D:\\'
disk2 = 'C:\\'

colors = {red, green, blue}
# init doodads
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((host, port))
# Functions
# Converts bytes to human readable values, Thanks Stackoverflow!
def humanSize(num):
	exp_str = [(0, 'B'), (10, 'K'),(20, 'M'),(30, 'G'),(40, 'T'), (50, 'P'),]
	i = 0
	while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
		i += 1
		rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
	return '%s%s' % (int(rounded_val), exp_str[i][1])

try:
	while 1:
		# CPU Usage data
		cpuUsage = psutil.cpu_percent(interval = 1)
		data = 'CPU: ' + repr(int(cpuUsage)) + '%'
		while len(data) < 9:
			data += ' '

		# Disk Usage data
		total1, used1, free1, percent1 = psutil.disk_usage(disk1)
		total2, used2, free2, percent2 = psutil.disk_usage(disk2)
		data += '\nC:/ ' + humanSize(used2) + '/' + humanSize(total2)

		if cpuUsage <= 25:
			color = cyan
		elif cpuUsage > 25 and cpuUsage <= 50:
			color = green
		elif cpuUsage <= 75 and cpuUsage > 50:
			color = yellow
		elif cpuUsage > 75:
			color = red

		sdata = ('message', data)
		scolor = ('color', color)

		sock.sendto(pickle.dumps(sdata, protocol = 2), (host, port))
		sock.sendto(pickle.dumps(scolor, protocol = 2), (host, port))
		time.sleep(0.1)
except KeyboardInterrupt:
	print("Ctrl-C Recived, Stopping!")

finally:
	sock.close()
