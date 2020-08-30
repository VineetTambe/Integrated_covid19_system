import LCD_buzzer as lcd
import cv2
from pyzbar import pyzbar
from smbus2 import SMBus
from mlx90614 import MLX90614


# Barcode Detection
barcode_text = ''
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
while True:
    ret, frame = camera.read()
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_text = barcode.data.decode('utf-8')
        print(barcode_text)
        lcd.write_msg(barcode_text)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('Barcode reader', frame)
    if len(barcode_text) != 0:
        break
camera.release()
cv2.destroyAllWindows()



#Face Mask Detection

nose_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('/home/pi/Desktop/final_integrate/dataXML/Mouth.xml')
counter = 0
if nose_cascade.empty():
  raise IOError('Unable to load the nose cascade classifier xml file')
cap = cv2.VideoCapture(0)
ds_factor = 0.5
pred=0
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
    mouth_rects = mouth_cascade.detectMultiScale(gray,1.3,5)
    if(len(nose_rects)!=0 and len(mouth_rects)!=0):
        for (x, y, w, h) in nose_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            break
        for (x, y, w, h) in mouth_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            break
        #print("No Mask")
        pred-=1
    else:
        #print("Mask")
        pred+=1
    #print(counter)
    counter = counter + 1
    if(counter==50):
        break
    cv2.imshow('Mask Detector', frame)




    c = cv2.waitKey(1)
    if c == 27:
        break

if pred>0:
    print("FINAL - MASK")
    lcd.write_msg("Mask Detected")
else:
    print("FINAL - NO MASK")
    lcd.write_warning("No Mask Detected")
        
cap.release()
cv2.destroyAllWindows()



#Temperature Detection

#bus = SMBus(1)
#sensor = MLX90614(bus, address=0x5A)
#avg_temp=0.0
#for i in range(0,50):
#    temp=sensor.get_object_1()
#    print (temp)
#    avg_temp+=temp
#avg_temp/=50
#if(avg_temp>37.77):
#    print("Temp- HIGH")
#    lcd.write_warning("Temp= "+str(avg_temp))   
#else:
#    print("Temp- LOW")
#    lcd.write_msg("Temp= "+str(avg_temp)) 



    
    


