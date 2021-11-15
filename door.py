import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def getDistance(TRIG,ECHO):
    #print('Distance measurement in Progress')
    #GPIO.output(TRIG,False)
    
    GPIO.output(TRIG,True)
    time.sleep(0.0001)
    GPIO.output(TRIG,False)
    pulse_start=0
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
        
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print(distance)
    return distance

if __name__=="__main__":
    cred = credentials.Certificate('doorsense-f9327d1a0fb5.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    TRIG=4
    ECHO=26
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    slot=db.collection('DoorDistance').document('1')
    try:
        while(True):
            doorDist=getDistance(TRIG,ECHO)
            slot.set({
                'distance':doorDist,  
            })
    except KeyboardInterrupt:
        print("Exit")

    

      