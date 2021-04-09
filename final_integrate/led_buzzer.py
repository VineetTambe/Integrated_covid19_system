from time import sleep
import RPi.GPIO as GPIO

class LEDBuzzer:
    def __init__(self):
        GPIO.setwarnings(False)         #disable warnings
        GPIO.setmode(GPIO.BOARD)

        buzzerpin = 12  # buzzer pin = 12
        self.led1g = 29
        self.led1r = 31
        self.led2g = 19
        self.led2r = 21
        self.led3g = 11
        self.led3r = 13

        GPIO.setup(self.led1r, GPIO.OUT)
        GPIO.setup(self.led1g, GPIO.OUT)
        GPIO.setup(self.led2r, GPIO.OUT)
        GPIO.setup(self.led2g, GPIO.OUT)
        GPIO.setup(self.led3r, GPIO.OUT)
        GPIO.setup(self.led3g, GPIO.OUT)
        GPIO.setup(buzzerpin,GPIO.OUT)
        self.pi_pwn = GPIO.PWM(buzzerpin,1000)
        self.set_all_low()

    def buzzer_success(self):
        self.pi_pwn.ChangeDutyCycle(100)
        sleep(1)
        self.pi_pwn.ChangeDutyCycle(0)
        sleep(1)
    
    def buzzer_warn(self):
        for i in range(0,21):
            self.pi_pwn.ChangeDutyCycle(50)
            sleep(0.1)
            self.pi_pwn.ChangeDutyCycle(0)
            sleep(0.1)

    def set_all_low(self):
        self.pi_pwn.start(0)
        GPIO.output(self.led1r, GPIO.LOW)
        GPIO.output(self.led1g, GPIO.LOW)
        GPIO.output(self.led2r, GPIO.LOW)
        GPIO.output(self.led2g, GPIO.LOW)
        GPIO.output(self.led3r, GPIO.LOW)
        GPIO.output(self.led3g, GPIO.LOW)

    def set_led1green(self):
        GPIO.output(self.led1g,GPIO.HIGH)
        self.buzzer_success()

    def set_led1red(self):
        GPIO.output(self.led1r, GPIO.HIGH)
        self.buzzer_warn()

    def set_led2green(self):
        GPIO.output(self.led2g, GPIO.HIGH)
        self.buzzer_success()

    def set_led2red(self):
        GPIO.output(self.led2r, GPIO.HIGH)
        self.buzzer_warn()

    def set_led3green(self):
        GPIO.output(self.led3g, GPIO.HIGH)
        self.buzzer_success()

    def set_led3red(self):
        GPIO.output(self.led3r, GPIO.HIGH)
        self.buzzer_warn()