import sys
import time

import cv2
import face_recognition
import numpy as np


def get_frame(stream, resizefactor=2):
    # Grab a single frame of video
    _, frame = stream.read()
    f = 1/resizefactor

    # Resize frame of video to 1/4 size for faster face recognition processing
    resized = cv2.resize(frame, (0, 0), fx=f, fy=f)

    # Convert the image from BGR color (which OpenCV uses) 
    # to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    return rgb_frame
 
def locate_faces(frame, model="hog"):
    return face_recognition.face_locations(frame, model=model)

# boolean function to regulate frameskipping
def get_index(frameno, frameskip=0):
    return frameno % (frameskip+1)

def to_process(frameno):
    return not bool(frameno)

# if detects a face in the picture before timeout, return it
# unlike the main event loop, here cnn is used, to increase
# accuracy.
def ensure(stream, resizefactor=2, timeout=3, frameskip=0):
    
    curr=0
    detected=None
    timeout = time.time() + timeout   
    
    while timeout > time.time() and not detected:
        
        curr = get_index(curr, frameskip)

        print(f"frame: [{curr}] "+"(%.2f)" %(time.time()-timeout))
        if to_process(curr):
            frame = get_frame(stream, resizefactor)
            detected = locate_faces(frame, "cnn")
        curr+=1

    return detected


def cleanup(stream, exitcode):

    stream.release()
    print(f"goodbye. ({exitcode})")
    sys.exit(exitcode)


# vars init
timeout = 4
resize = 4
frameskip = 4
sleepiness = .5
face_locations = []

# Get a reference to webcam #0 (the default one)
videostream = cv2.VideoCapture(0)
curr = 0

while True:
    
    curr = get_index(curr, frameskip)

    # Only process when the frame index is modular to frameskip 
    if to_process(curr):
        frame = get_frame(videostream, resize)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = locate_faces(frame)
    

        if face_locations:
            curr+=1
            time.sleep(sleepiness)
            continue
        
        # If no face are to be found, ensure is not hog model limit
        if not ensure(videostream, resize, timeout, frameskip):
            break
        
    curr += 1

cleanup(videostream, 0)
