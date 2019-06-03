import serial
import RPi.GPIO as GPIO
import time
import sys
R =16
G=17
B=18
BuzzPin = 14
def setup(pin):
   global BuzzerPin
   BuzzerPin = pin
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(BuzzerPin, GPIO.OUT)
   GPIO.setup(R,GPIO.OUT)
   GPIO.setup(G,GPIO.OUT)
   GPIO.setup(B,GPIO.OUT)
   GPIO.output(BuzzerPin, GPIO.LOW)
   GPIO.output(R, GPIO.LOW)
   GPIO.output(G, GPIO.LOW)
   GPIO.output(B, GPIO.LOW)

   
def on():
   GPIO.output(BuzzerPin, GPIO.HIGH)
def off():
   GPIO.output(BuzzerPin, GPIO.LOW)
def destroy():
   GPIO.output(BuzzerPin,GPIO.LOW)
   GPIO.cleanup()
def loop():
   id1=0
   id2=0
   id3=0
   id4=0
   while True:
         reci=serialFromArduino.readline()
         reci=float(reci)
         print(reci)
         if reci==1:
               on()
               GPIO.output(R, GPIO.HIGH)
               id1+=1
               print(id1)
               time.sleep(1)
               off()
               GPIO.output(R,GPIO.LOW)
         elif reci==2:
               on()
               GPIO.output(G,GPIO.HIGH)
               id2+=1
               print(id2)
               time.sleep(1)
               off()
               GPIO.output(G,GPIO.LOW)
         elif reci ==3:
            on()
            GPIO.output(B,GPIO.HIGH)
            id3+=1
            print(id3)
            time.sleep(1)
            off()
            GPIO.output(B,GPIO.LOW)
         elif reci ==4:
            on()
            GPIO.output(R,GPIO.HIGH)
            GPIO.output(B,GPIO.HIGH)
            id4+=1
            print(id4)
            time.sleep(1)
            off()
            GPIO.output(R,GPIO.LOW)
            GPIO.output(B,GPIO.LOW)
port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(port,9600)
serialFromArduino.flushInput()
if __name__ == '__main__':
      setup(BuzzPin)
      try:
         loop()
      except KeyboardInterrupt:
         destroy()
