#!/usr/bin/env python
import sys

################################################################################
#           script for sending and receiving messages to/from MBTemp
################################################################################

# print tes.__repr__() --> print without proccessing characters (\n, \r, \x, etc...)
# print tes.__str__()  --> print the proccessed message

################################################
#           setup of the serial port
################################################

import serial
connection = serial.Serial("/dev/ttyUSB0", 19200, timeout=1)
print "\n"
print "  ================================================="
print "  |                SENDING MESSAGE                |"
print "  ================================================="

################################################################################

################################################
#   calculate checksum and SEND the message
################################################

# reads the destination address of the message
print "  |                                               |"
print "  | ADRESSING: what is the destination?           |"
sys.stdout.write('  |     - 0x')
destination = raw_input()               # receive user input through keyboard
destination = destination.upper()       # convert lower case to upper
print "\x1b[1A",						# move cursor up
print "\x1b[2K",						# erase line
print "|     - 0x" + destination + "                                    |"
destination_str = destination           # make a copy of the input string
destination_int = int(destination,16)   # change from string to integer
destination = chr(int(destination,16))  # change from integer to hexadecimal (one bytes)

# reads the command to send
print "  | MESSAGE: what is the command?                 |"
sys.stdout.write('  |     - 0x')
command = raw_input()                   # receive user input through keyboard
command = command.upper()	        	# convert lower case to upper
print "\x1b[1A",						# move cursor up
print "\x1b[2K",						# erase line
print "|     - 0x" + command + "                                    |"
command_str = command                   # make a copy of the input string
command_int = int(command,16)           # change from string to integer
command = chr(int(command,16))          # change from integer to hexadecimal (one bytes)

# reads the length of the payload
print "  | MESSAGE: what is the length?                  |"
sys.stdout.write('  |     - 0x')
length = raw_input()
length = length.upper()					# convert lower case to upper
print "\x1b[1A",						# move cursor up
print "\x1b[2K",						# erase line
print "|     - 0x" + length + "                                  |"
# divide lenght in two bytes
byte_length_1 = length[0:2]
byte_length_2 = length[2:4]
# make a copy of the input string
byte_length_1_str = byte_length_1
byte_length_2_str = byte_length_2
# change from string to integer
byte_length_1_int = int(byte_length_1,16)
byte_length_2_int = int(byte_length_2,16)
# change from integer to hexadecimal (one bytes)
byte_length_1 = chr(int(byte_length_1,16))
byte_length_2 = chr(int(byte_length_2,16))

# if payload doesn't exist, show the followig message
if ((byte_length_1 == "\x00") and (byte_length_2 == "\x00")):
	print "  | MESSAGE: there is no payload!                 |"
	payload = ""
	payload_checksum = 0;

# if payload exists, ask for its bytes
else:
	print "  | MESSAGE: what is the payload?                 |"
	sys.stdout.write('  |     - 0x')
	payload = raw_input()
	payload = payload.upper()			# convert lower case to upper
	print "\x1b[1A",						# move cursor up
	print "\x1b[2K",						# erase line
	print "|     - 0x" + payload + "                                    |"

	payload_checksum = 0
	# splits payload in groups of two characters (one byte)
	bytes_of_payload = [payload[i:i+2] for i in range(0, len(payload), 2)]
	# sum all of these groups (all of bytes)
	for i in range(len(payload)/2):
		payload_checksum = payload_checksum + int(bytes_of_payload[i], 16)

# sum of all of the bytes of the packet
checksum = (destination_int + command_int + byte_length_1_int + byte_length_2_int + payload_checksum) % 0x100
checksum = (0x100 - checksum) % 0x100
# represent checksum in hex (2 digits)
checksum_str = "{:02X}".format(checksum)
checksum = chr(checksum)
print "  | CHECKSUM: the checksum is:                    |"
print "  |     - 0x%s" %checksum_str + "                                    |"
print "  |                                               |"

# put the first 4 bytes of the message in "message_to_send"
message_to_send = "%s%s%s%s" % (destination, command, byte_length_1, byte_length_2)
message_to_print = r"\x%s\x%s\x%s\x%s" %(destination_str, command_str, byte_length_1_str, byte_length_2_str)
# if payload is not empty, join its bytes with the message
if payload != "":
	# clear string message_payload
	message_payload = ""
	for i in range(len(payload)/2):
		# join the first 4 bytes with the payload
		message_to_send = "".join(["%s", "%s"]) %(message_to_send, chr(int(bytes_of_payload[i], 16)))
		message_to_print = r"\x".join(["%s", "%s"]) %(message_to_print, (bytes_of_payload[i]))

# join the last byte (checksum) to "message_to_send"
message_to_send = "".join(["%s", "%s"]) %(message_to_send, checksum)
message_to_print = r"\x".join(["%s", "%s"]) %(message_to_print, checksum_str)

# prints "connection.write("...")" and all of the bytes of the message
print '  | connection.write("%s")  |' %message_to_print
print "  |                                               |"

# send the message to MBTemp
connection.write("%s" %message_to_send)

################################################################################

################################################
#   RECEIVE the message and check checksum
################################################

print "  ================================================="
print "  |               RECEIVING MESSAGE               |"
print "  ================================================="

#answer = connection.read(20)
message_received = ""
next_byte = connection.read(1)
# after read the first byte, set the timeout to 100ms
connection.timeout = 0.1
# keep reading bytes until timeout exceed
while (next_byte != ""):
	message_received += next_byte
	next_byte = connection.read(1)

# fix the bytes recognised as a symbol in ASCII table
i = 0
answer = ""
while (i < len(message_received)):
	aux = "{:02x}".format(ord(message_received[i]))
	answer = r"\x".join(["%s", "%s"]) %(answer, aux)
	i += 1

################################

if (answer == ""):
	print "  |                                               |"
	print "  | Timeout passed: no message received           |"
	print "  |                                               |"

else:
	#answer = connection.read(1)             # read the answered message
	#answer = answer.__repr__()              # representation without proccessing
	#answer = answer.replace(r"\n", r"\x0A") # substitute "\n" with "\x0A"
	original_message = answer               # save the original message to show later
	answer = answer.replace(r"\x", "")      # substitute "\x" with nothing
	#answer = answer.replace("'", "")        # substitute "'" with "nothing
	answer_bytes = (len(answer) / 2)        # calculate number of bytes

	# separate the message in group of bytes (two nibbles)
	answer = [answer[i:i+2] for i in range(0, len(answer), 2)]

	# converts each element of the vector answer to the format "0x__"
	for i in range (answer_bytes):
		answer[i] = r"0x%s" %answer[i]

	# calculates the checksum of the answer message
	checksum_answer = 0;
	for i in range (answer_bytes - 1):
		checksum_answer = checksum_answer + int(answer[i], 16)

	# sum checksum_answer with last byte of message and compare with 0x00
	checksum_answer = (checksum_answer + int(answer[answer_bytes - 1], 16)) % 0x100
	if checksum_answer != 0:
		print "  |                                               |"
		print "  | Message corrupted: Checksum not equal to 0x00 |"
		print "  |                                               |"
	else:
		print "  |                                               |"
		print "  | connection.read()                             |"
		# convert lower-case to upper-case letter
		original_message = original_message.replace("a", "A")
		original_message = original_message.replace("b", "B")
		original_message = original_message.replace("c", "C")
		original_message = original_message.replace("d", "D")
		original_message = original_message.replace("e", "E")
		original_message = original_message.replace("f", "F")
		# print original message received
		print "  | " + original_message + "                  |"
		print "  |                                               |"
'''
		####################################################
		# Decoding received message for calibration purpose
		####################################################

		# if the message received is a reading value from a variable (0x11), then decode the message --> mostly used for calibration of MBtemp
		if ((answer[0] == "0x00") & (answer[1] == "0x11") & (answer[2] == "0x00") & (answer[3] == "0x02")):
			# reading the variable ALPHA
			if (payload == "08"):  
				# take only the positions referent to the 2 bytes of payload
				sys.stdout.write("  | Alpha = 0x")
			elif (payload == "09"):	  # reading the SLOPE k
				sys.stdout.write("  |   k   = 0x")
			elif (payload == "0A"):	  # reading the COEFFICIENT b
				sys.stdout.write("  |   b   = 0x")
			print original_message[18] + original_message[19] + original_message[22] + original_message[23] + "                                |"
			print "  |                                               |"
'''

print "  ================================================="
print "\n"



