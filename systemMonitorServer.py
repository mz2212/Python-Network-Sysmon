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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.bind((host, port))
# Listen for a client wanting to send LCD data
sock.listen(1)
print("Press Ctrl-C to stop the server")

try:
	while 1:
		conn, addr = sock.accept()
		print(addr[0] + ":" + str(addr[1]) + " connected!")
		while 1:
			try:
				# 16 * 2 * 8 = 256, or is it just 32? Bits/bytes?
				data = conn.recv(256)
				color = conn.recv(64)

			except socket.error:
				break

			else:
				if data:
					lcd.clear()
					# The problem
					lcd.message(data)
					print("Successfully wrote " + data + " to the display!")
					if color:
						lcd.set_color(pickle.loads(color))
				else:
					break

except KeyboardInterrupt:
	# Handle Ctrl-C
	print("Ctrl-C Recived, Stopping!")
finally:
	# Cleanup
	sock.close()
	lcd.clear()
