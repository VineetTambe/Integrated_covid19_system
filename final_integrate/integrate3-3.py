from led_buzzer import LEDBuzzer
import os
# os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)
import cv2 
#import RPi.GPIO as GPIO
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

# TODO: test on actual system

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

class IntegratedSystem:
    def __int__(self):
        # led and buzzer init
        self.buzz = LEDBuzzer()

        #firebase setup
        self.cred = credentials.Certificate('python-firebase-upload-firebase-adminsdk-rmqdn-c62596b24a.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.now = datetime.now()
        #print(now)
        firebase = pyrebase.initialize_app(config)
        self.storage = firebase.storage()

        #CSV for data reference
        self.csv = open("barcode.csv", "a")
        self.csv1 = open("temp.csv", "a")

        #I2C temperature sensor
        bus = SMBus(1)
        self.sensor = MLX90614(bus, address=0x5A)
        self.greetings = ["Have a great Day!", "Have a Wonderful Day!", "Welcome to PICT!", "Hope to see you again!",
                     "Hello and Welcome!"]
        self.name = ''
        self.threshold = 37.77

        # Face Mask Detection
        self.camera = cv2.VideoCapture(0)
        self.nose_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/haarcascade_mcs_nose.xml')

    def firebase_upload(self,img):
        # This function will upload the passed image to the dir of the current date
        today = datetime.now()
        path_cloud = str(today.date())+"/"+str(today.strftime('%Y-%m-%d %H:%M:%S'))+"-facemask-"+" "+str(img)
        self.storage.child(path_cloud).put(img)

    def upload(self,time,enr,temp):
        doc_ref = self.db.collection(str(self.now.strftime("%Y-%m-%d"))).document()
        doc_vio = self.db.collection(str(self.now.strftime("%Y-%m-%d"))+'-critical').document()
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

    def wait_for_barcode(self):
        barcode_text = ""
        # 0 indicates that webcam associated with device
        # 1,2 can be used for external webcam
        # camera = cv2.VideoCapture(0)
        ret, frame = self.camera.read()
        while ret:
            ret, frame = self.camera.read()
            # frame = read_barcodes(frame)
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                x, y, w, h = barcode.rect
                barcode_text = barcode.data.decode('utf-8')
                # print(barcode_text)
                name = SearchCSV.get_name(barcode_text.lstrip("0"))
                print("Hello ", name)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Barcode reader', frame)
            if (len(barcode_text) == 3 or len(barcode_text) == 6 or len(barcode_text) == 11 or len(
                    barcode_text) == 5 or len(barcode_text) == 4 or len(barcode_text) == 1 or len(barcode_text) == 2):
                # print("1")
                # GPIO.output(led1g,GPIO.HIGH)
                self.buzz.set_led1green()
                return barcode_text
            else:
                pass

            if cv2.waitKey(1) & 0xFF == 27:
                return
            else:
                pass

    def detect_nose(self):
        # camera.release()
        # cv2.destroyAllWindows()
        i = 0
        # mouth_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/Mouth.xml')
        counter = 0
        if self.nose_cascade.empty():
            raise IOError('Unable to load the nose cascade classifier xml file')
            # camera = cv2.VideoCapture(0)
        else:
            pass

        ds_factor = 0.5
        pred = 0

        while True:

            ret, frame = self.camera.read()
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if counter % 3 == 0:
                nose_rects = self.nose_cascade.detectMultiScale(gray, 1.3, 5)
                # mouth_rects = mouth_cascade.detectMultiScale(gray,1.3,5)
                if (len(nose_rects) != 0):
                    for (x, y, w, h) in nose_rects:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        break
                    # for (x, y, w, h) in mouth_rects:
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # break
                    # print("No Mask")
                    pred -= 1
                else:
                    # print("Mask")
                    pred += 1
                    # print(counter)
            else:
                pass

            counter = counter + 1

            if (counter == 60):
                return pred,frames
            else:
                pass
            cv2.imshow('Mask Detector', frame)
            c = cv2.waitKey(1)
            if c == 27:
                return
            else:
                pass

    def calc_temperature(self):
        ambient = self.sensor.get_ambient()
        # print('Ambient- ',ambient)
        if ambient >= 31:
            factor = 37.5 / ambient
        elif 29 <= ambient < 31:
            factor = 36.5 / ambient
        elif 27 <= ambient < 29:
            factor = 36 / ambient
        elif 25 <= ambient < 27:
            factor = 35 / ambient
        elif 23 <= ambient < 25:
            factor = 33 / ambient
        elif 21 <= ambient < 23:
            factor = 30 / ambient
        elif 19 <= ambient < 21:
            factor = 28.5 / ambient
        else:
            factor = 34 / ambient
        # factor=1.30
        # print('Factor-',factor)
        avg_temp = 0.0
        for i in range(0, 50):
            temp = self.sensor.get_object_1()
            # print (temp)
            avg_temp += temp
        avg_temp /= 50
        # print('Temp before factor- ',avg_temp)
        avg_temp *= factor
        # print('Temp after factor- ',avg_temp)
        avg_temp1 = avg_temp
        if avg_temp < 35:
            avg_temp1 = 35 + (avg_temp - math.floor(avg_temp))

        print("The ambient temperature is ", ambient, "C")
        print("Your temperature is ", avg_temp1, " C")

        self.csv1.write("{},{},{},{},{}\n".format(datetime.now(), ambient, factor, (avg_temp / factor), avg_temp1))
        return avg_temp1

    def run(self):
        self.buzz.set_all_low()

        #Barcode Detetcion
        barcode_text = self.wait_for_barcode()
        if barcode_text is None:
            raise IOError
        else:
            pass

        #nose Detection
        pred , frame = self.detect_nose()
        # print(pred)
        if pred is None:
            raise IOError
        else:
            pass

        if pred > 10:
            print("FINAL - MASK")
            # GPIO.output(led2g,GPIO.HIGH)
            self.buzz.set_led2green()
        else:
            cv2.imwrite(os.path.join('/home/pi/Desktop/Integrate/', barcode_text + '.jpg'), frame)
            print("FINAL - NO MASK")
            # GPIO.output(led2r,GPIO.HIGH)
            self.buzz.set_led2red()
            # self.firebase_upload(barcode_text+'.jpg')

        # camera.release()
        # cv2.destroyAllWindows()


        ## Temperature Detection
        time.sleep(2)
        # bus = SMBus(1)
        # sensor = MLX90614(bus, address=0x5A)
        # threshold=(ambient+2)*factor
        avg_temp = self.calc_temperature()
        # print('Threshold- ',threshold)
        if avg_temp > self.threshold:
            print("Temperature- HIGH")
            # GPIO.output(led3r,GPIO.HIGH)
            self.buzz.set_led3green()
        else:
            # print("Temperature- NORMAL")
            # GPIO.output(led3g,GPIO.HIGH)
            self.buzz.set_led3red()

        print(self.greetings[np.random.randint(0, 4)])
        self.csv.write("{},{},{},{}\n".format(datetime.now(), self.barcode_text, self.name, avg_temp))

        # current_time = now.strftime("%d/%m/%Y %H:%M:%S") #timestamp
        # print(now)
        # current_time=datetime.now()

        # self.upload(now,barcode_text,avg_temp)
        self.csv.flush()
        self.csv1.flush()

    def on_shutdown(self):
        self.buzz.set_all_low()
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    integrated_obj = IntegratedSystem()
    try:
        while True:
            integrated_obj.run()
    except IOError as e:
        integrated_obj.on_shutdown()
        print('Run time error occured: %s' , e)

