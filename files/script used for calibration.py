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
print "  |         READIND VARIABLES FROM MBtemp         |"
print "  ================================================="

################################################################################

################################################
#   calculate checksum and SEND the message
################################################

# reads the destination address of the message
print "  |                                               |"
print "  | What is the MBtemp address?                   |"
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
#print "  | MESSAGE: what is the command?                 |"
#sys.stdout.write('  |     - 0x')
#command = raw_input()                  # receive user input through keyboard
#command = command.upper()	        	# convert lower case to upper
#print "\x1b[1A",						# move cursor up
#print "\x1b[2K",						# erase line
#print "|     - 0x" + command + "                                    |"
command = "10"
command_str = command                   # make a copy of the input string
command_int = int(command,16)           # change from string to integer
command = chr(int(command,16))          # change from integer to hexadecimal (one bytes)

# reads the length of the payload
#print "  | MESSAGE: what is the length?                  |"
#sys.stdout.write('  |     - 0x')
#length = raw_input()
#length = length.upper()				# convert lower case to upper
#print "\x1b[1A",						# move cursor up
#print "\x1b[2K",						# erase line
#print "|     - 0x" + length + "                                  |"
length = "0001"
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
#if ((byte_length_1 == "\x00") and (byte_length_2 == "\x00")):
#	print "  | MESSAGE: there is no payload!                 |"
#	payload = ""
#	payload_checksum = 0;

# if payload exists, ask for its bytes
#else:
#	print "  | MESSAGE: what is the payload?                 |"
#	sys.stdout.write('  |     - 0x')
#	payload = raw_input()
#	payload = payload.upper()			# convert lower case to upper
#	print "\x1b[1A",						# move cursor up
#	print "\x1b[2K",						# erase line
#	print "|     - 0x" + payload + "                                    |"

################################################################################
# Sending the message to read ALPHA

payload_alpha = "08"
payload_checksum_alpha = 0

# splits payload in groups of two characters (one byte)
bytes_of_payload_alpha = [payload_alpha[i:i+2] for i in range(0, len(payload_alpha), 2)]
# sum all of these groups (all of bytes)
for i in range(len(payload_alpha)/2):
	payload_checksum_alpha = payload_checksum_alpha + int(bytes_of_payload_alpha[i], 16)

# sum of all of the bytes of the packet
checksum_alpha = (destination_int + command_int + byte_length_1_int + byte_length_2_int + payload_checksum_alpha) % 0x100
checksum_alpha = (0x100 - checksum_alpha) % 0x100
# represent checksum in hex (2 digits)
checksum_alpha_str = "{:02X}".format(checksum_alpha)
checksum_alpha = chr(checksum_alpha)
#print "  | CHECKSUM: the checksum is:                    |"
#print "  |     - 0x%s" %checksum_alpha_str + "                                    |"
#print "  |                                               |"

# put the first 4 bytes of the message in "message_to_send"
message_to_send_alpha = "%s%s%s%s" % (destination, command, byte_length_1, byte_length_2)
message_to_print_alpha = r"\x%s\x%s\x%s\x%s" %(destination_str, command_str, byte_length_1_str, byte_length_2_str)
# if payload is not empty, join its bytes with the message
if payload_alpha != "":
	# clear string message_payload
	message_payload = ""
	for i in range(len(payload_alpha)/2):
		# join the first 4 bytes with the payload
		message_to_send_alpha = "".join(["%s", "%s"]) %(message_to_send_alpha, chr(int(bytes_of_payload_alpha[i], 16)))
		message_to_print_alpha = r"\x".join(["%s", "%s"]) %(message_to_print_alpha, (bytes_of_payload_alpha[i]))

# join the last byte (checksum) to "message_to_send"
message_to_send_alpha = "".join(["%s", "%s"]) %(message_to_send_alpha, checksum_alpha)
message_to_print_alpha = r"\x".join(["%s", "%s"]) %(message_to_print_alpha, checksum_alpha_str)

# prints "connection.write("...")" and all of the bytes of the message
print "  |                                               |"
print '  | connection.write("%s")  |' %message_to_print_alpha

# send the message to MBTemp
#connection.write("%s" %message_to_send_alpha)

################################################################################
# Sending the message to read K

payload_k = "09"
payload_checksum_k = 0

# splits payload in groups of two characters (one byte)
bytes_of_payload_k = [payload_k[i:i+2] for i in range(0, len(payload_k), 2)]
# sum all of these groups (all of bytes)
for i in range(len(payload_k)/2):
	payload_checksum_k = payload_checksum_k + int(bytes_of_payload_k[i], 16)

# sum of all of the bytes of the packet
checksum_k = (destination_int + command_int + byte_length_1_int + byte_length_2_int + payload_checksum_k) % 0x100
checksum_k = (0x100 - checksum_k) % 0x100
# represent checksum in hex (2 digits)
checksum_k_str = "{:02X}".format(checksum_k)
checksum_k = chr(checksum_k)
#print "  | CHECKSUM: the checksum is:                    |"
#print "  |     - 0x%s" %checksum_k_str + "                                    |"
#print "  |                                               |"

# put the first 4 bytes of the message in "message_to_send"
message_to_send_k = "%s%s%s%s" % (destination, command, byte_length_1, byte_length_2)
message_to_print_k = r"\x%s\x%s\x%s\x%s" %(destination_str, command_str, byte_length_1_str, byte_length_2_str)
# if payload is not empty, join its bytes with the message
if payload_k != "":
	# clear string message_payload
	message_payload = ""
	for i in range(len(payload_k)/2):
		# join the first 4 bytes with the payload
		message_to_send_k = "".join(["%s", "%s"]) %(message_to_send_k, chr(int(bytes_of_payload_k[i], 16)))
		message_to_print_k = r"\x".join(["%s", "%s"]) %(message_to_print_k, (bytes_of_payload_k[i]))

# join the last byte (checksum) to "message_to_send"
message_to_send_k = "".join(["%s", "%s"]) %(message_to_send_k, checksum_k)
message_to_print_k = r"\x".join(["%s", "%s"]) %(message_to_print_k, checksum_k_str)

# prints "connection.write("...")" and all of the bytes of the message
print '  | connection.write("%s")  |' %message_to_print_k
#print "  |                                               |"

# send the message to MBTemp
#connection.write("%s" %message_to_send_k)

################################################################################
# Sending the message to read b

payload_b = "0A"
payload_checksum_b = 0

# splits payload in groups of two characters (one byte)
bytes_of_payload_b = [payload_b[i:i+2] for i in range(0, len(payload_b), 2)]
# sum all of these groups (all of bytes)
for i in range(len(payload_b)/2):
	payload_checksum_b = payload_checksum_b + int(bytes_of_payload_b[i], 16)

# sum of all of the bytes of the packet
checksum_b = (destination_int + command_int + byte_length_1_int + byte_length_2_int + payload_checksum_b) % 0x100
checksum_b = (0x100 - checksum_b) % 0x100
# represent checksum in hex (2 digits)
checksum_b_str = "{:02X}".format(checksum_b)
checksum_b = chr(checksum_b)
#print "  | CHECKSUM: the checksum is:                    |"
#print "  |     - 0x%s" %checksum_b_str + "                                    |"
#print "  |                                               |"

# put the first 4 bytes of the message in "message_to_send"
message_to_send_b = "%s%s%s%s" % (destination, command, byte_length_1, byte_length_2)
message_to_print_b = r"\x%s\x%s\x%s\x%s" %(destination_str, command_str, byte_length_1_str, byte_length_2_str)
# if payload is not empty, join its bytes with the message
if payload_b != "":
	# clear string message_payload
	message_payload = ""
	for i in range(len(payload_b)/2):
		# join the first 4 bytes with the payload
		message_to_send_b = "".join(["%s", "%s"]) %(message_to_send_b, chr(int(bytes_of_payload_b[i], 16)))
		message_to_print_b = r"\x".join(["%s", "%s"]) %(message_to_print_b, (bytes_of_payload_b[i]))

# join the last byte (checksum) to "message_to_send"
message_to_send_b = "".join(["%s", "%s"]) %(message_to_send_b, checksum_b)
message_to_print_b = r"\x".join(["%s", "%s"]) %(message_to_print_b, checksum_b_str)

# prints "connection.write("...")" and all of the bytes of the message
print '  | connection.write("%s")  |' %message_to_print_b
print "  |                                               |"

# send the message to MBTemp
#connection.write("%s" %message_to_send_b)

################################################################################
################################################################################

################################################
#   RECEIVE the message and check checksum
################################################

print "  ================================================="
print "  |               RECEIVING MESSAGE               |"
print "  ================================================="

################################################################################

# Receiving the message to read alpha
connection.write("%s" %message_to_send_alpha)

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
#	print "  |                                               |"

else:
	#answer = connection.read(1)             # read the answered message
	#answer = answer.__repr__()              # representation without proccessing
	#answer = answer.replace(r"\n", r"\x0A") # substitute "\n" with "\x0A"
	original_message_alpha = answer               # save the original message to show later
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
#		print "  |                                               |"
	else:
		print "  |                                               |"
		print "  | connection.read()                             |"
		# convert lower-case to upper-case letter
		original_message_alpha = original_message_alpha.replace("a", "A")
		original_message_alpha = original_message_alpha.replace("b", "B")
		original_message_alpha = original_message_alpha.replace("c", "C")
		original_message_alpha = original_message_alpha.replace("d", "D")
		original_message_alpha = original_message_alpha.replace("e", "E")
		original_message_alpha = original_message_alpha.replace("f", "F")
		# print original message received
		print "  | " + original_message_alpha + "                  |"
#		print "  |                                               |"

################################################################################

# Receiving the message to read k
connection.write("%s" %message_to_send_k)

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
#	print "  |                                               |"

else:
	#answer = connection.read(1)             # read the answered message
	#answer = answer.__repr__()              # representation without proccessing
	#answer = answer.replace(r"\n", r"\x0A") # substitute "\n" with "\x0A"
	original_message_k = answer               # save the original message to show later
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
#		print "  |                                               |"
	else:
#		print "  |                                               |"
#		print "  | connection.read()                             |"
		# convert lower-case to upper-case letter
		original_message_k = original_message_k.replace("a", "A")
		original_message_k = original_message_k.replace("b", "B")
		original_message_k = original_message_k.replace("c", "C")
		original_message_k = original_message_k.replace("d", "D")
		original_message_k = original_message_k.replace("e", "E")
		original_message_k = original_message_k.replace("f", "F")
		# print original message received
		print "  | " + original_message_k + "                  |"
#		print "  |                                               |"

################################################################################

# Receiving the message to read b
connection.write("%s" %message_to_send_b)

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
#	print "  |                                               |"

else:
	#answer = connection.read(1)             # read the answered message
	#answer = answer.__repr__()              # representation without proccessing
	#answer = answer.replace(r"\n", r"\x0A") # substitute "\n" with "\x0A"
	original_message_b = answer               # save the original message to show later
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
#		print "  |                                               |"
	else:
#		print "  |                                               |"
#		print "  | connection.read()                             |"
		# convert lower-case to upper-case letter
		original_message_b = original_message_b.replace("a", "A")
		original_message_b = original_message_b.replace("b", "B")
		original_message_b = original_message_b.replace("c", "C")
		original_message_b = original_message_b.replace("d", "D")
		original_message_b = original_message_b.replace("e", "E")
		original_message_b = original_message_b.replace("f", "F")
		# print original message received
		print "  | " + original_message_b + "                  |"
		print "  |                                               |"

################################################################################

		####################################################
		# Decoding received message for calibration purpose
		####################################################
'''
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

alpha = original_message_alpha[18] + original_message_alpha[19] + original_message_alpha[22] + original_message_alpha[23]
k = original_message_k[18] + original_message_k[19] + original_message_k[22] + original_message_k[23]
b = original_message_b[18] + original_message_b[19] + original_message_b[22] + original_message_b[23]

#  --> Alpha = e
#14
#  -->   k   = e
#  -->   b   = e

################################
#		Printing ALPHA
################################
sys.stdout.write("  | Alpha = 0x")
print alpha + " =",
alpha = int(alpha,16)
print alpha,

# spaces after INTEGER number is printed, depending on the number of digits
if (len(str(alpha)) == 5):
	print "",
if (len(str(alpha)) == 4):
	print " ",
elif (len(str(alpha)) == 3):
	print "  ",
elif (len(str(alpha)) == 2):
	print "   ",
elif (len(str(alpha)) == 1):
	print "    ",

# prepare to show integer number divided by 100
print "-->  Alpha =",
alpha = float(alpha)/100
print alpha,

# spaces after DECIMAL number is printed, depending on the number of digits
if (len(str(alpha)) == 6):
	print "",
if (len(str(alpha)) == 5):
	print " ",
elif (len(str(alpha)) == 4):
	print "  ",
elif (len(str(alpha)) == 3):
	print "   ",
elif (len(str(alpha)) == 2):
	print "    ",
elif (len(str(alpha)) == 2):
	print "    ",
print " |"
################################
#			Printing k
################################
sys.stdout.write("  |   k   = 0x")
print k + " =",
print (int(k,16)),
if (len(str(int(k,16))) == 5):
	print "",
if (len(str(int(k,16))) == 4):
	print " ",
elif (len(str(int(k,16))) == 3):
	print "  ",
elif (len(str(int(k,16))) == 2):
	print "   ",
elif (len(str(int(k,16))) == 1):
	print "    ",

# prepare to show integer number divided by 100
print "-->    k   =",
k = float(int(k,16))/100
print k,

# spaces after DECIMAL number is printed, depending on the number of digits
if (len(str(k)) == 6):
	print "",
if (len(str(k)) == 5):
	print " ",
elif (len(str(k)) == 4):
	print "  ",
elif (len(str(k)) == 3):
	print "   ",
elif (len(str(k)) == 2):
	print "    ",
elif (len(str(k)) == 2):
	print "    ",
print " |"

################################
#			Printing b
################################
sys.stdout.write("  |   b   = 0x")
print b + " =",
print (int(b,16)),
if (len(str(int(b,16))) == 5):
	print "",
if (len(str(int(b,16))) == 4):
	print " ",
elif (len(str(int(b,16))) == 3):
	print "  ",
elif (len(str(int(b,16))) == 2):
	print "   ",
elif (len(str(int(b,16))) == 1):
	print "    ",

# prepare to show integer number divided by 100
print "-->    b   =",
b = float(int(b,16))/100
print b,

# spaces after DECIMAL number is printed, depending on the number of digits
if (len(str(b)) == 6):
	print "",
if (len(str(b)) == 5):
	print " ",
elif (len(str(b)) == 4):
	print "  ",
elif (len(str(b)) == 3):
	print "   ",
elif (len(str(b)) == 2):
	print "    ",
elif (len(str(b)) == 2):
	print "    ",
print " |"

################################################################################

print "  |                                               |"
print "  ================================================="
print "\n"



