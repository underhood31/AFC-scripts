from pylsl import StreamInfo, StreamOutlet
import random
import time
import csv
import keyboard

def main():

    # Set up LabStreamingLayer stream.
    info = StreamInfo(name='PyMarker', type='Markers', channel_count=3,
                      channel_format='double64', source_id='unique113')

    # Broadcast the stream.       
    outlet = StreamOutlet(info)

    print("Now sending data...")

    markerValue = 1
    prev = -1
    while (True):
        if keyboard.is_pressed(" ") and (time.time()-prev) > 2:
            
            prev = time.time()
            markerValue+=1
            print("Marker value: ", markerValue,"\tMarker time: ", now)

        now = time.time()
        


        # data: MarkerTime, MarkerValue, Current EpochTime
        data = [now, markerValue, now]
        
        # push data 
        outlet.push_sample(data)

        time.sleep(0.05)

if __name__ == "__main__":
    main()