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
			header, data = pickle.loads(sock.recv(256))

		except socket.error:
			break

		else:
			if data:
				lcd.clear()
				# The problem
				if header == 'message':
					lcd.message(data)
					print("Successfully wrote " + data + " to the display!")
				if header == 'color':
					red, green, blue = data
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
