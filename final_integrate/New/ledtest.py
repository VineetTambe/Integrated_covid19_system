import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)         #disable warnings
GPIO.setmode(GPIO.BOARD)
led1g = 29
led1r = 31
led2g = 19
led2r = 21
led3g = 11
led3r = 13
GPIO.setup(led1r,GPIO.OUT)
GPIO.setup(led1g,GPIO.OUT)
GPIO.setup(led2r,GPIO.OUT)
GPIO.setup(led2g,GPIO.OUT)
GPIO.setup(led3r,GPIO.OUT)
GPIO.setup(led3g,GPIO.OUT)
while True:
    print("LED on")
    GPIO.output(led1r,GPIO.HIGH)
    time.sleep(5)
    print( "LED off")
    GPIO.output(led1r,GPIO.LOW)
    time.sleep(5)
    print("LED on")
    GPIO.output(led2r,GPIO.HIGH)
    time.sleep(5)
    print( "LED off")
    GPIO.output(led2r,GPIO.LOW)
    time.sleep(5)
    print("LED on")
    GPIO.output(led3r,GPIO.HIGH)
    time.sleep(5)
    print( "LED off")
    GPIO.output(led3r,GPIO.LOW)
    time.sleep(5)