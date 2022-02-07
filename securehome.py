import RPi.GPIO as GPIO
import time
from tkinter import Image
from firebase_admin import storage
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
    
    firebase_admin.initialize_app(cred, {
    'storageBucket': 'doorsense.appspot.com'
    })

    db = firestore.client()
    IMAGE_NAME = 'image.jpeg'
    cam=Camera(IMAGE_NAME,100,100)
    
    bucket = storage.bucket()
    blob=bucket.blob('image.jpeg')
    
    MotionSensor=Pir(4)
    motion=0
    #blob.download_to_filename('image.jpg')
    slot=db.collection('SecureHome').document('1')
    
    try:
        while(True):
            motion=MotionSensor.detectMotion()
            slot.update({
                'Motion':motion  
            })
            if(motion==1):
                print('Motion')
                h_w=slot.get().to_dict()['res']
                cam.setResolution(h_w,h_w)                
                cam.capture()
                blob.upload_from_filename('image.jpeg')

            time.sleep(2)
    except KeyboardInterrupt:
        print("Exit")

      