from gtts import gTTS
from tkinter import *
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import *

def play_read_instructions(file):
    from pygame import mixer
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

def no_motion_for_read():
    

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    
    num_of_detections = 2 # count down to zero to report no movement
    
    while num_of_detections > 0:
        k = 0
        for i in range(800000):
            k += int(GPIO.input(4))
        if k == 0:
            num_of_detections -= 1
    return True

def snap_picture():
    camera = PiCamera()
    sleep(5)
    camera.color_effects = (128,128)
    camera.capture('image.jpg')
    camera.stop_preview()

def read_captured_text(read_text):
   myob=gTTS(text=read_text,lang='en',slow=False)
   myob.save('read_text.mp3')
   play_read_instructions('read_text.mp3')



def read_mode():
    print('When ready, place text in front of camera')
    play_read_instructions("read_instructions.mp3")
    error_count = 0
    while True:
        if no_motion_for_read():
            snap_picture()
            break
        else:
            print('Please, hold still')
            play_read_instructions('hold_still.mp3')
        if error_count > 2:
            print('A still shot could not be taken')
            play_read_instructions('no_shot_due_to_movement.mp3')
            return
    text = pytesseract.image_to_string(Image.open('image.jpg'))
    print('Snapshot taken. Please wait while I process text.')
    play_read_instructions('processing_text.mp3')
    if len(text) == 0:
        print('No readable text found!')
        play_read_instructions('no_text.mp3')
    else:
        sleep(2)
        read_captured_text(text)
    





read_mode()


















