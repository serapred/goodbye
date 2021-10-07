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
 
def locate_faces(frame):
    return face_recognition.face_locations(frame)

# boolean function to regulate frameskipping
def index_frame(frameno, frameskip):
    return frameno % (frameskip+1)

def to_process(frameno):
    return not bool(frameno)

# if detects a face in the picture before timeout, return it
def ensure(stream, resizefactor=2, timeout=3):
    
    detected=None
    timeout = time.time() + timeout
    
    while timeout > time.time() and not detected:
        print(timeout-time.time())
        frame = get_frame(stream, resizefactor)
        detected = locate_faces(frame)

    return detected


def cleanup(stream, exitcode):

    stream.release()
    print(f"goodbye. ({exitcode})")
    sys.exit(exitcode)

# vars init
timeout = 4
resize=3
frameskip=2
current=0
face_locations = []

# Get a reference to webcam #0 (the default one)
videostream = cv2.VideoCapture(0)

while True:
    current = index_frame(current, frameskip)
    # Only process every other frame of video to save time
    
    if to_process(current):
        frame = get_frame(videostream, resize)
        # Find all the faces and face encodings in the current frame of video
        face_locations = locate_faces(frame)
        
        if not face_locations:
            result = ensure(videostream, timeout)
            print(f"result: {result}")
            if not result:
                cleanup(videostream, 1)

cleanup(videostream, 0)
