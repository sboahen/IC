import RPi.GPIO as GPIO
import cv2
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
from math import ceil
import time

def play_read_instructions(file):
    from pygame import mixer
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

def distance():
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 24

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
#    print('Waiting for sensor to settle')
    time.sleep(0.8)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #print("Distance:", distance, "cm")
    GPIO.cleanup()
    return distance


def face_detection():
    start = time.time()
    cwd = os.getcwd()

    face_cascade = cv2.CascadeClassifier(cwd + '/haarcascades/' +'haarcascade_frontalface_default.xml')

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 40
    rawCapture = PiRGBArray(camera, size=(640, 480))
 
    # allow the camera to warmup
    time.sleep(0.1)

    face_count = 0
    loop_count = 0

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
    
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.8, 3)
        # commented out for speed -- can be brought back for display if needed
#        for (x,y,w,h) in faces:
#            image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)  
#        cv2.imshow('det', image)
 
        face_count += len(faces)
        loop_count += 1
        if loop_count == 5:
            curr_distance = distance()
            num_of_faces =(ceil(face_count/6))
            if curr_distance < 60 and num_of_faces != 0:
                print('Someone is too near you')
                play_read_instructions('near_you.mp3')
                time.sleep(0.1)
            elif curr_distance < 60:
                print('Obstruction detected!')
                play_read_instructions('obstruction.mp3')
                time.sleep(0.1)
            elif num_of_faces > 0:
                if num_of_faces > 1:
                    print('Multiple faces detected')
                    play_read_instructions('multiple_faces.mp3')
                    time.sleep(0.1)
                else:
                    print('face detected')
                    play_read_instructions('single_face.mp3')
                    time.sleep(0.1)
            
            loop_count = face_count = 0
        
        
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        if time.time() - start > 20:
            break 
    cv2.destroyAllWindows()
    return
            
    


face_detection()
#main()
#print(distance())
  














