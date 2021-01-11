import LCD_buzzer as lcd 
import os
# os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)
import cv2 
import RPi.GPIO as GPIO
from pyzbar import pyzbar
import datetime
import time
from smbus2 import SMBus
from mlx90614 import MLX90614
import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import SearchCSV
import numpy as np
import pyrebase
import math

cred = credentials.Certificate('python-firebase-upload-firebase-adminsdk-rmqdn-c62596b24a.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
now = datetime.now()
#print(now)

config = {
    "apiKey": "AIzaSyBSo0u4CQ1_V0_Bn-Ml8TI_8wi2DlUP_lc",
    "authDomain": "python-firebase-upload.firebaseapp.com",
    "databaseURL": "https://python-firebase-upload.firebaseio.com",
    "projectId": "python-firebase-upload",
    "storageBucket": "python-firebase-upload.appspot.com",
    "messagingSenderId": "453107651670",
    "appId": "1:453107651670:web:ff28b2b8976b7f767797f7",
    "measurementId": "G-PFVT7NE4W6",
    "serviceAccount": "python-firebase-upload-firebase-adminsdk-rmqdn-c62596b24a.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def firebase_upload(img):
    # This function will upload the passed image to the dir of the current date
	today = datetime.now()
	path_cloud = str(today.date())+"/"+str(today.strftime('%Y-%m-%d %H:%M:%S'))+"-facemask-"+" "+str(img)
	storage.child(path_cloud).put(img)

def upload(time,enr,temp):
	doc_ref = db.collection(str(now.strftime("%Y-%m-%d"))).document()
	doc_vio = db.collection(str(now.strftime("%Y-%m-%d"))+'-critical').document()
	doc_ref.set({
		'Time':time,
		'Enrollment Number':enr,
		'Temperature':temp 
	})
	if (float(temp) > 37.5):
		doc_vio.set({
			'Time':time,
			'Enrollment Number':enr,
			'Temperature':temp
		})


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
csv1=open("temp.csv","a")
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
greetings=["Have a great Day!","Have a Wonderful Day!","Welcome to PICT!","Hope to see you again!","Hello and Welcome!"]
name=''


while True:
    GPIO.output(led1r,GPIO.LOW)
    GPIO.output(led1g,GPIO.LOW)
    GPIO.output(led2r,GPIO.LOW)
    GPIO.output(led2g,GPIO.LOW)
    GPIO.output(led3r,GPIO.LOW)
    GPIO.output(led3g,GPIO.LOW)
    GPIO.output(12,GPIO.HIGH)
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
            #print(barcode_text)
            name=SearchCSV.get_name(barcode_text.lstrip("0"))
            print("Hello ",name)
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
        cv2.imshow('Barcode reader', frame)
        if(len(barcode_text)==3 or len(barcode_text)==6 or len(barcode_text)==11 or len(barcode_text)==5 or len(barcode_text)==4 or len(barcode_text)==1 or len(barcode_text)==2):
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
        if(counter%3==0):
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
    #print(pred)
    if pred>10:
        print("FINAL - MASK")
        GPIO.output(led2g,GPIO.HIGH)
        lcd.write_msg("Mask Detected")
    else:
        cv2.imwrite(os.path.join('/home/pi/Desktop/Integrate/',barcode_text+'.jpg'),frame)
        print("FINAL - NO MASK")
        GPIO.output(led2r,GPIO.HIGH)
        lcd.write_warning("No Mask Detected")
        #firebase_upload(barcode_text+'.jpg')
        
        
    #camera.release()
    #cv2.destroyAllWindows()
    #Temperature Detection
    time.sleep(2)
    #bus = SMBus(1)
    #sensor = MLX90614(bus, address=0x5A)
    ambient=sensor.get_ambient()
    #print('Ambient- ',ambient)
    if(ambient>=31):
        factor=37.5/ambient
    elif(ambient>=29 and ambient<31):
        factor=36.5/ambient    
    elif(ambient>=27 and ambient<29):
        factor=36/ambient
    elif(ambient>=25 and ambient<27):
        factor=35/ambient
    elif(ambient>=23 and ambient<25):
        factor=33/ambient
    elif(ambient>=21 and ambient<23):
        factor=30/ambient
    elif(ambient>=19 and ambient<21):
        factor=28.5/ambient
    else:
        factor= 34/ambient
    #factor=1.30
    #print('Factor-',factor)
    avg_temp=0.0
    for i in range(0,50):
        temp=sensor.get_object_1()
        #print (temp)
        avg_temp+=temp
    avg_temp/=50
    #print('Temp before factor- ',avg_temp)
    avg_temp*=factor
    #print('Temp after factor- ',avg_temp)
    avg_temp1=avg_temp
    if(avg_temp<35):
        avg_temp1=35+(avg_temp - math.floor(avg_temp))
    
    print("The ambient temperature is ",ambient,"C")
    print ("Your temperature is ",avg_temp1," C")
   
    #threshold=(ambient+2)*factor
    threshold=37.77
    #print('Threshold- ',threshold)
    if(avg_temp>threshold):
        print("Temperature- HIGH")
        GPIO.output(led3r,GPIO.HIGH)
        lcd.write_warning("Temp= "+str(avg_temp))   
    else:
        #print("Temperature- NORMAL")
        GPIO.output(led3g,GPIO.HIGH)
        lcd.write_msg("Temp= "+str(avg_temp)) 
    
    print(greetings[np.random.randint(0,4)])
    csv.write("{},{},{},{}\n".format(datetime.now(),barcode_text,name,avg_temp1))
    csv1.write("{},{},{},{},{}\n".format(datetime.now(),ambient,factor,(avg_temp/factor),avg_temp))
    #current_time = now.strftime("%d/%m/%Y %H:%M:%S") #timestamp
    #print(now)
    #current_time=datetime.now()
    
    #upload(now,barcode_text,avg_temp)
    csv.flush()
    csv1.flush()
    
camera.release()
cv2.destroyAllWindows()