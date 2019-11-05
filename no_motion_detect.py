
def no_motion_for_read():
    import RPi.GPIO as GPIO
    from time import sleep

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

print(no_motion_for_read())