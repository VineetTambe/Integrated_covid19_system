import LCD_buzzer as lcd 
import cv2
import os
import RPi.GPIO as GPIO
from pyzbar import pyzbar
import datetime
import time
from smbus2 import SMBus
from mlx90614 import MLX90614
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
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
# Barcode Detection
# import the necessary packages
camera = cv2.VideoCapture(0)
csv = open("barcode.csv","a")
while True:
    GPIO.output(led1r,GPIO.LOW)
    GPIO.output(led1g,GPIO.LOW)
    GPIO.output(led2r,GPIO.LOW)
    GPIO.output(led2g,GPIO.LOW)
    GPIO.output(led3r,GPIO.LOW)
    GPIO.output(led3g,GPIO.LOW)
    barcode_text=""
    # 0 indicates that webcam associated with device
    # 1,2 can be used for external webcam
    #camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        #frame = read_barcodes(frame)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_text = barcode.data.decode('utf-8')
            print(barcode_text)
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
        cv2.imshow('Barcode reader', frame)
        if(len(barcode_text)==3 or len(barcode_text)==11 or len(barcode_text)==5 or len(barcode_text)==4 or len(barcode_text)==1 or len(barcode_text)==2):
            #print("1")
            GPIO.output(led1g,GPIO.HIGH)
            lcd.write_msg("barcode detected")
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break

    #camera.release()
    #cv2.destroyAllWindows()
    i = 0
    #Face Mask Detection

    nose_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/haarcascade_mcs_nose.xml')
    #mouth_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/Mouth.xml')
    counter = 0
    if nose_cascade.empty():
        raise IOError('Unable to load the nose cascade classifier xml file')
        #camera = cv2.VideoCapture(0)
    ds_factor = 0.5
    pred=0
    while True:
        ret, frame = camera.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
        #mouth_rects = mouth_cascade.detectMultiScale(gray,1.3,5)
        if(len(nose_rects)!=0):
            for (x, y, w, h) in nose_rects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                break
            #for (x, y, w, h) in mouth_rects:
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                #break
            #print("No Mask")
            pred-=1
        else:
            #print("Mask")
            pred+=1
            #print(counter)
        counter = counter + 1
        if(counter==60):
            break
        cv2.imshow('Mask Detector', frame)
        c = cv2.waitKey(1)
        if c == 27:
            break
    print(pred)
    if pred>-30:
        print("FINAL - MASK")
        GPIO.output(led2g,GPIO.HIGH)
        lcd.write_msg("Mask Detected")
    else:
        cv2.imwrite(os.path.join('/home/pi/Desktop/final_integrate/Image',barcode_text + '.jpg'), frame)
        print("FINAL - NO MASK")
        GPIO.output(led2r,GPIO.HIGH)
        lcd.write_warning("No Mask Detected")
        
        
    #camera.release()
    #cv2.destroyAllWindows()
#Temperature Detection
    time.sleep(3)
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    avg_temp=0.0
    for i in range(0,50):
        temp=sensor.get_object_1()
        #print (temp)
        avg_temp+=temp
    avg_temp/=50
    #print(avg_temp)
    print(avg_temp*3.33)
    avg_temp=avg_temp*3.33
    if(avg_temp>100):
        print("Temp- HIGH")
        GPIO.output(led3r,GPIO.HIGH)
        lcd.write_warning("Temp= "+str(avg_temp))   
    else:
        print("Temp- LOW")
        GPIO.output(led3g,GPIO.HIGH)
        lcd.write_msg("Temp= "+str(avg_temp)) 
    
    csv.write("{},{},{}\n".format(datetime.datetime.now(),barcode_text,avg_temp))
    csv.flush()
    
camera.release()
cv2.destroyAllWindows()