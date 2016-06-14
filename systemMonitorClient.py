# Imports
import time
import socket
import psutil
import pickle
import threading

# Vars
host = '192.168.11.200'
client = ''
port = 7166
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
yellow = (1, 1, 0)
magenta = (1, 0, 1)
cyan = (0, 1, 1)
white = (1, 1, 1)
off = (0, 0, 0)
disk1 = 'C:\\'
disk2 = 'D:\\'
disk3 = 'E:\\'
state = 'U'
threadRun = 1
clear = 1
spaces = ('clear', 'doot')
onOff = 1
# init doodads
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.connect((host, port))
sock.bind((client, port))
# Functions
# Converts bytes to human readable values, Thanks Stackoverflow!
def humanSize(num):
	exp_str = [(0, 'B'), (10, 'K'),(20, 'M'),(30, 'G'),(40, 'T'), (50, 'P'),]
	i = 0
	while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
		i += 1
		rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
	return '%s%s' % (int(rounded_val), exp_str[i][1])

# Listens for button presses and changes a variable
def listenForButtons():
	while threadRun:
		header, data = pickle.loads(sock.recv(256))
		# Debugging
		#print(header)
		if header == 'button':
			global state
			state = data
			global clear
			clear = 1
		if header == 'select':
			global onOff
			if onOff:
				onOff = 0
			else:
				onOff = 1

t = threading.Thread(target=listenForButtons, args=())
try:
	t.start()
except:
	print("Failed to start listener thread... Just CPU usage sent.")
try:
	while 1:
		if state == 'U':
			# Cleanup the display if needed
			if clear:
				sock.sendto(pickle.dumps(spaces, protocol = 2), (host, port))
				clear = 0
			# CPU Usage data
			cpuUsage = psutil.cpu_percent(interval = 1)
			data = 'CPU: ' + repr(int(cpuUsage)) + '%'
			while len(data) < 9:
				data += ' '

			# RAM usage data
			mem = psutil.virtual_memory()
			data += '\nRAM: ' + humanSize(mem.used) + '/' + humanSize(mem.total)

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

		if state == 'R':
			if clear:
				sock.sendto(pickle.dumps(spaces, protocol = 2), (host, port))
				clear = 0
			# Disk Usage data
			time.sleep(5)
			total1, used1, free1, percent1 = psutil.disk_usage(disk1)
			total2, used2, free2, percent2 = psutil.disk_usage(disk2)
			total3, used3, free3, percent3 = psutil.disk_usage(disk3)

			data = 'C:/ ' + humanSize(used1) + '/' + humanSize(total1)
			data +='\nE:/ ' + humanSize(used3) + '/' + humanSize(total3)

			scolor = ('color', cyan)
			sdata = ('message', data)
		if not onOff:
			scolor = ('color', off)
		sock.sendto(pickle.dumps(sdata, protocol = 2), (host, port))
		sock.sendto(pickle.dumps(scolor, protocol = 2), (host, port))
		time.sleep(0.1)
except KeyboardInterrupt:
	print("Ctrl-C Recived, Stopping!")

finally:
	threadRun = 0
	sock.close()
