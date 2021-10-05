import face_recognition
import cv2
import numpy as np
import sys
import time 

    
def acquire():
    # Grab a single frame of video
    _, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) 
    # to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    return rgb_frame
 

def ensure(timeout, exitcode=125):
    timeout = time.time() + timeout
    while True:
        frame = acquire()
        if face_recognition.face_locations(frame):
            return
        if time.time() > timeout:
            video_capture.release()
            print("Goodbye!")
            sys.exit(exitcode)

# in seconds
timeout = 2

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
process_this_frame = True


while True:

    frame = acquire()
    # Only process every other frame of video to save time
    if process_this_frame:   
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)

    if not face_locations:
        ensure(timeout)
    
    process_this_frame = not process_this_frame

# Release handle to the webcam
video_capture.release()
