#!/usr/bin/python
# libs
import time
import Adafruit_CharLCD as LCD
import socket
import pickle
import threading

# Variables
host = ''
port = 7166
client = '192.168.11.202'
threadRun = 1
oldData = 'abcdefghijklmnopqrstuvwxyzABCDEF'
column = 0
row = 0
loc = 0

# init doodads
lcd = LCD.Adafruit_CharLCDPlate()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buttons = ((LCD.SELECT, 'K'), (LCD.LEFT, 'L'),
 (LCD.UP, 'U'), (LCD.RIGHT, 'R'), (LCD.DOWN, 'D'))

sock.bind((host, port))
# Listen for a client wanting to send LCD data

# Functions
# Poll the buttons and send a packet if one is pressed
def pollReply():
	while threadRun:
		for button in buttons:
			if lcd.is_pressed(button[0]):
				if button[0] is not LCD.SELECT:
					sData = ('button', button[1])
					sock.sendto(pickle.dumps(sData, protocol = 2), (client, port))
					time.sleep(0.15)
				else:
					sData = ('select', button[1])
					time.sleep(0.3)
					sock.sendto(pickle.dumps(sData, protocol = 2), (client, port))
					time.sleep(0.3)
		time.sleep(0.15)

t = threading.Thread(target=pollReply, args=())
try:
	t.start()
except:
	print("Failed to start button poller, Won't send button presses!")

print("Press Ctrl-C to stop the server")

try:
	while 1:
		try:
			# 16 * 2 * 8 = 256, or is it just 32? Bits/bytes?
			header, data = pickle.loads(sock.recv(256))

		except socket.error:
			break

		else:
			if data:
				if header == 'message':
					for char in data:
						if char == '\n':
							column = 0
							row = 1
						elif oldData[loc] == char:
							if column >= 15:
								column = 0
								row = 1
								column += 1
								loc += 1
							else:
								column +=1
								loc += 1
						else:
							lcd.set_cursor(column, row)
							lcd.message(char)
							if column >= 15:
								column = 0
								row = 1
								column += 1
								loc += 1
							else:
								column += 1
								loc += 1
					oldData = data
					while len(oldData) < 32:
						oldData += ' '
					column = 0
					row = 0
					loc = 0
					# Debugging
					#print("Successfully wrote " + data + " to the display!")
				if header == 'color':
					red, green, blue = data
					lcd.set_color(red, green, blue)
				if header == 'clear':
					lcd.clear()
					oldData = ''
					while len(oldData) < 32:
						oldData += ' '

except KeyboardInterrupt:
	# Handle Ctrl-C
	print("Ctrl-C Recived, Stopping!")
finally:
	# Cleanup
	threadRun = 0
	sock.close()
	lcd.clear()
	lcd.set_color(0, 0, 0)
