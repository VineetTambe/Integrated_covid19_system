from RPLCD.gpio import CharLCD
from time import sleep
import RPi.GPIO as GPIO

buzzerpin = 12                  #buzzer pin = 12
GPIO.setwarnings(False)         #disable warnings
GPIO.setmode(GPIO.BOARD)        
GPIO.setup(buzzerpin,GPIO.OUT)
pi_pwn = GPIO.PWM(buzzerpin,1000)
lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
            numbering_mode=GPIO.BOARD)
pi_pwn.start(0)


def write_msg(message):
    #lcd.clear()
    #lcd.cursor_pos = (1,0)
    #lcd.write_string(message)
    pi_pwn.ChangeDutyCycle(100)
    sleep(1)
    pi_pwn.ChangeDutyCycle(0)
    sleep(1)
    #lcd.clear()

def write_warning(message):
    #lcd.clear()
    #lcd.cursor_pos = (1,0)
    #lcd.write_string(message)
    for i in range(0,21):
        pi_pwn.ChangeDutyCycle(50)
        sleep(0.1)
        pi_pwn.ChangeDutyCycle(0)
        sleep(0.1)
    #lcd.clear()


