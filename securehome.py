import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from camera import Camera

class Pir:
    signal=4
    def __init__(self,signal):
        self.signal=signal
        GPIO.setup(self.signal,GPIO.IN)
        
        
    def detectMotion(self):
        if(GPIO.input(self.signal)):
            return 1
        else:
            return 0
        

if __name__=="__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    cred = credentials.Certificate('doorsense-f9327d1a0fb5.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    MotionSensor=Pir(4)
    motion=0
    slot=db.collection('SecureHome').document('1')
    try:
        while(True):
            motion=MotionSensor.detectMotion()         
            slot.set({
                'Motion':motion  
            })
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit")

    

      