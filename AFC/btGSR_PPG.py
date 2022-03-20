#!/usr/bin/python
import sys, struct, serial
import time
from csv import writer
import os

# os.mkdir('D:/ADHD-Protocol/Phase2_DATA/'+sys.argv[2])
timestr = time.strftime("%Y%m%d-%H%M%S")
# filename = ('D:/ADHD-Protocol/Phase2_DATA/'+sys.argv[2])+"/GSR_" + sys.argv[2] +"_"+ timestr + ".csv"
filename = ('D:/ADHD-Protocol/Phase2_DATA')+"/GSR_" + sys.argv[2] +"_"+ timestr + ".csv"

def wait_for_ack():
	ddata = ""
	ack = struct.pack('B', 0xff)
	while ddata != ack:
		ddata = ser.read(1)
		print(ddata[0])
	  
	return

if len(sys.argv) < 2:
	print( "no device specified")
	print( "You need to specify the serial port of the device you wish to connect to")
	print( "example:")
	print( "   aAccel5Hz.py Com12")
	print( "or")
	print( "   aAccel5Hz.py /dev/rfcomm0")
else:
	ser = serial.Serial(sys.argv[1], 115200)
	ser.flushInput()
	print( "port opening, done.")
	# csv_file = open(filename, "w")
	# csv_file.write("Timestamp,GSR,PPG\n")
	# csv_file.write("a,1\nb,2\nc,3")

# send the set sensors command
	ser.write(struct.pack('BBBB', 0x08 , 0x04, 0x01, 0x00))  #GSR and PPG
	wait_for_ack()   
	print( "sensor setting, done.")

# Enable the internal expansion board power
	ser.write(struct.pack('BB', 0x5E, 0x01))
	wait_for_ack()
	print( "enable internal expansion board power, done.")

# send the set sampling rate command

	'''
	 sampling_freq = 32768 / clock_wait = X Hz
	'''
	sampling_freq = 128
	clock_wait = (2 << 14) / sampling_freq
	# print(type(0x05))
	# print(type(clock_wait))
	ser.write(struct.pack('<BH', 0x05, int(clock_wait)))
	# ser.write(struct.pack(0x05, clock_wait))
	wait_for_ack()

# send start streaming command
	ser.write(struct.pack('B', 0x07))
	wait_for_ack()
	print( "start command sending, done.")

# read incoming data
	ddata = ""
	numbytes = 0
	framesize = 8 # 1byte packet type + 3byte timestamp + 2 byte GSR + 2 byte PPG(Int A13)

	print( "Packet Type\tTimestamp\tGSR\tPPG")
	try:
		with open(filename, 'a') as f:
		
			w = writer(f)
			try:
				while True:
					while numbytes < framesize:
						ddata += str(ser.read(framesize))
						numbytes = len(ddata)
					
					data = ddata[0:framesize]
					ddata = ddata[framesize:]
					numbytes = len(ddata)

					# read basic packet information
					# print(type(data))
					(packettype) = struct.unpack('B', str.encode(data[0:1]))
					(timestamp0, timestamp1, timestamp2) = struct.unpack('BBB', str.encode(data[1:4]))

					# read packet payload
					(PPG_raw, GSR_raw) = struct.unpack('HH', str.encode(data[4:framesize]))

					# get current GSR range resistor value
					Range = ((GSR_raw >> 14) & 0xff)  # upper two bits
					if(Range == 0):
						Rf = 40.2   # kohm
					elif(Range == 1):
						Rf = 287.0  # kohm
					elif(Range == 2):
						Rf = 1000.0 # kohm
					elif(Range == 3):
						Rf = 3300.0 # kohm

					# convert GSR to kohm value
					gsr_to_volts = (GSR_raw & 0x3fff) * (3.0/4095.0)
					GSR_ohm = Rf/( (gsr_to_volts /0.5) - 1.0)

					# convert PPG to milliVolt value
					PPG_mv = PPG_raw * (3000.0/4095.0)

					# timestamp = timestamp0 + timestamp1*256 + timestamp2*65536
					timestamp = time.time()
					# print( "0x%02x\t\t%5d,\t%4d,\t%4d" % (packettype[0], timestamp, GSR_ohm, PPG_mv))
					print( "Timestamp %5d,\t GSR %4d,\t PPG %4d" % (timestamp, GSR_ohm, PPG_mv))
					finaldata = [timestamp, GSR_ohm, PPG_mv]
					# finaldata = [timestamp, GSR_ohm, PPG_mv]

					
					w.writerow(finaldata)
			except KeyboardInterrupt:
				ser.write(struct.pack('B', 0x20))
				print()
				print( "stop command sent, waiting for ACK_COMMAND")
				wait_for_ack()
				print( "ACK_COMMAND received.")
		#close serial port
				ser.close()
				print( "All done")

		f.close()

	except KeyboardInterrupt:
#send stop streaming command
		ser.write(struct.pack('B', 0x20))
		print()
		print( "stop command sent, waiting for ACK_COMMAND")
		wait_for_ack()
		print( "ACK_COMMAND received.")
#close serial port
		ser.close()
		print( "All done")
