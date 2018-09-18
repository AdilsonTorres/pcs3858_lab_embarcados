import RPi.GPIO as GPIO

import time
from picamera import PiCamera


def button_callback(channel):
    print("photo taken")
    # Blink led
    GPIO.output(11, 1)
    time.sleep(1)
    GPIO.output(11, 0)
    # Capture photo
    camera.capture('image.jpg')


# Led pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = PiCamera()

GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) 


message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up



