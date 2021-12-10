"""
Video to Serial
Author: Dallin Poole
Purpose:
    Use OpenCV to detect faces within the camera and convert that into a yaw angle to be sent over serial to arduino.
"""

import multiprocessing as mp 
import cv2
import numpy as np
import serial
import time

# Camera's FOV
FOV = 100
# Camera's horizontal resolution
WIDTH = 1280 / 2

# UART connection to Arduino.
# Use the port found in Arduino IDE or device manager.
serial_port = 'COM6'
arduino = serial.Serial(port=serial_port, baudrate=115200, timeout=.1)

# Send value over to the arduino board and listen back for confirmation.
def send_to_arduino( value ):    
    value = str(value) + "\n"
    arduino.write(bytes(value, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data)

# Setup our camera
def make_capture():
    # open webcam video stream
    cap = cv2.VideoCapture(0)
    return cap

# Handle Video Input
def video_in( ):
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # Recognizes the front of a face.
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = make_capture()

    #Create a display for the frames we handle.
    cv2.startWindowThread()

    while( True ):
        # Handy hotkey to exit out.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Capture frame-by-frame
        ret, frame = cap.read()
        # Handle the frame.
        if frame is not None:
            frame_calc( frame, face_cascade )
            
    

    # When everything done, release the capture
    cap.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)




def frame_calc(frame, face_cascade):
    # detect people in the image
    # returns the bounding boxes for the detected objects
    # boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    boxes = face_cascade.detectMultiScale(gray, minNeighbors=20, minSize=(20,20))
    
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # Show our frame with faces that we've recognized
    cv2.imshow('frame', frame)     
    
    # Calculate the horizontal position of the face.
    sum = 0
    new_x_offset = 0
    
    if(len(boxes) > 0):
        for box in boxes:
            sum += (box[0] + box[2]) / 2
        
        new_x_offset = sum / len(boxes)
        send_to_arduino(int(FOV * (new_x_offset / WIDTH)))

    


if __name__ == '__main__':   
    video_in()

