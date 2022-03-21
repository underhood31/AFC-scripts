import time
import os
import random
pathStart="./Videos"

from pylsl import StreamInfo, StreamOutlet
import random
import time
import csv
import keyboard
import cv2
import numpy as np

def playVideo(path):
	# Create a VideoCapture object and read from input file
	cap = cv2.VideoCapture(path)

	# Check if camera opened successfully
	if (cap.isOpened()== False): 
	  print("Error opening video  file")
	   
	# Read until video is completed
	while(cap.isOpened()):
	      
	  # Capture frame-by-frame
	  ret, frame = cap.read()
	  if ret == True:
	   
	    # Display the resulting frame
	    cv2.imshow('Frame', frame)
	   
	    # Press Q on keyboard to  exit
	    if cv2.waitKey(25) & 0xFF == ord('q'):
	      break
	   
	  # Break the loop
	  else: 
	    break
	   
	# When everything done, release 
	# the video capture object
	cap.release()
	   
	# Closes all the frames
	cv2.destroyAllWindows()

if __name__ == '__main__':
	print("Start time:",time.time())

	# Set up LabStreamingLayer stream.
	info = StreamInfo(name='PyMarker', type='Markers', channel_count=2,
	                  channel_format='double64', source_id='unique113')

	# Broadcast the stream.       
	outlet = StreamOutlet(info)

	print("Now sending data...")

	markerValue = 1
	prev = -1

	#loop over all the videos
	allFolders=os.listdir(pathStart)
	random.shuffle(allFolders)
	for i,folder in enumerate(allFolders):
		allVideos=os.listdir(pathStart+"/"+folder)
		random.shuffle(allVideos)
		video=allVideos[0]
			

		print("Video:",i,"Name:",video,"Start time:",time.time())
		#run the video
		# os.system("totem "+"Videos/"+video)
		playVideo("Videos/"+folder+"/"+video)


		# Run the script to start the sensors
		# Do from Bat file

		print("Video:",i,"Name:",video,"End time:",time.time())
		

		now = time.time()
		data = [now, markerValue]

		# push data 
		outlet.push_sample(data)
		markerValue+=1
		print("Marker value: ", markerValue,"\tMarker time: ", now)


		input("Press enter to continue...")
		



	


		
