import argparse
import numpy as np
import cv2

from pylsl import StreamInlet, resolve_stream
import time

cap = cv2.VideoCapture(0) # Capture video from camera

parser = argparse.ArgumentParser(description="NAME")
parser.add_argument('name', type=str)
args = parser.parse_args()

name = args.name
filename = "../data/Webcam_"+name+"_"+time.strftime("%Y%m%d-%H%M%S")+".mp4"




# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
out = cv2.VideoWriter(filename  , fourcc, 20.0, (width, height))

streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0], max_buflen=6)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # frame = cv2.flip(frame,0)

        sample, timestamp = inlet.pull_sample()
        # sample, timestamp = inlet.pull_sample()
        font = cv2.FONT_HERSHEY_SIMPLEX 
        # print(type(sampl 

        marker_text = sample[0]

        if(str(marker_text)=="-1.0"):
        	 break
    # Use putText() method for 
    # inserting text on video 
        print(marker_text)
        cv2.putText(frame, str(marker_text), (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    else:
        break

# Release everything if job is finished
out.release()
cap.release()
cv2.destroyAllWindows()