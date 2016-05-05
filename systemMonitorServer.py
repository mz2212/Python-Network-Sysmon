#!/usr/bin/python
# libs
import time
import Adafruit_CharLCD as LCD
import socket
import pickle

# Variables
host = ''
port = 7166

# init doodads
lcd = LCD.Adafruit_CharLCDPlate()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind((host, port))
# Listen for a client wanting to send LCD data
print("Press Ctrl-C to stop the server")

try:
	while 1:
		try:
			# 16 * 2 * 8 = 256, or is it just 32? Bits/bytes?
			data = sock.recv(256)
			color = sock.recv(64)

		except socket.error:
			break

		else:
			if data:
				lcd.clear()
				# The problem
				lcd.message(data)
				print("Successfully wrote " + data + " to the display!")
				if color:
					red, green, blue = pickle.loads(color)
					lcd.set_color(red, green, blue)
			else:
				break

except KeyboardInterrupt:
	# Handle Ctrl-C
	print("Ctrl-C Recived, Stopping!")
finally:
	# Cleanup
	sock.close()
	lcd.clear()
	lcd.set_color(0, 0, 0)
