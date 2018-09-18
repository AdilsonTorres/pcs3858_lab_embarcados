import RPi.GPIO as GPIO

import time

on = False

def blink_led(channel):
    global on
    print("press button")
    if on:
        on = False
        GPIO.output(11, 1)
    else:
        on = True
        GPIO.output(11, 0)

# Led pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(10, GPIO.RISING, callback=blink_led)

message = input("Press enter to quit\n\n")

GPIO.cleanup()



