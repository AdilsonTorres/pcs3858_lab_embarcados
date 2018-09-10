import RPi.GPIO as GPIO

import time
from picamera import PiCamera

# Led pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT)


camera = PiCamera()

# Capture photo
camera.capture('image.jpg')

# Blink led
GPIO.output(40, 1)
time.sleep(1)
GPIO.output(40, 0)




