# import LCD_buzzer as lcd
import cv2
import csv
import datetime
import time
from pyzbar import pyzbar

# from smbus2 import SMBus
# from mlx90614 import MLX90614

#csv = open("barcode.csv", "a")


# Barcode Detection
# import the necessary packages
nose_cascade = cv2.CascadeClassifier('C:\\Users\\Shardul Khandekar\\Desktop\\final_integrate\\dataXML\\haarcascade_mcs_nose.xml')
#mouth_cascade = cv2.CascadeClassifier('C:\\Users\\Shardul Khandekar\\Desktop\\final_integrate\\dataXML\\Mouth.xml')

def main():
    barcode_text = ""
    # 0 indicates that webcam associated with device
    # 1,2 can be used for external webcam
    camera = cv2.VideoCapture(1)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        # frame = read_barcodes(frame)
        barcodes = pyzbar.decode(frame)
        cv2.rectangle(frame, (100, 250), (400, 300), (255, 0, 0))
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_text = barcode.data.decode('utf-8')
            print(barcode_text)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Barcode reader', frame)
        if (len(barcode_text) == 11):
            #csv.write("{},{}\n".format(datetime.datetime.now(), barcode_text))
            #csv.flush()
            #print("1")
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break

    i = 0
    # Face Mask Detection
    counter = 0
    if nose_cascade.empty():
        raise IOError('Unable to load the nose cascade classifier xml file')
    ds_factor = 0.5
    pred = 0
    while True:
        ret, frame = camera.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if(counter%3==0):
            nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
            # mouth_rects = mouth_cascade.detectMultiScale(gray, 1.3, 5)
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
        counter = counter + 1
        if (counter == 100):
            break
        cv2.imshow('Mask Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break
    print(pred)
    if pred >10:
        print("FINAL - MASK")
        # lcd.write_msg("Mask Detected")
    else:
        cv2.imwrite('kang' + str(i) + '.jpg', frame)
        print("FINAL - NO MASK")
        # lcd.write_warning("No Mask Detected")
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        main()

# Temperature Detection

# bus = SMBus(1)
# sensor = MLX90614(bus, address=0x5A)
# avg_temp=0.0
# for i in range(0,50):
# temp=sensor.get_object_1()
# print (temp)
# avg_temp+=temp
# avg_temp/=50
# if(avg_temp>37.77):
# print("Temp- HIGH")
# lcd.write_warning("Temp= "+str(avg_temp))
# else:
# print("Temp- LOW")
# lcd.write_msg("Temp= "+str(avg_temp))






