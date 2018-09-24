import RPi.GPIO as GPIO
import dht11
import time
from datetime import datetime
import pyrebase

config={
    "apiKey": "AIzaSyB_ifeBeXX1Zh9uni8mg2BiFgCgwvTK4co",
    "authDomain": "motion-sensor-test.firebaseapp.com",
    "databaseURL": "https://motion-sensor-test.firebaseio.com",
    "storageBucket": "motion-sensor-test.appspot.com",
    }

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()
user = auth.sign_in_with_email_and_password("motiondetection@gmail.com", "motiondetection")



# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=6)

temp=instance.read()
while True:
    if temp.is_valid(): 
            x=str(datetime.now());
            test={"Time" : x, "Temperature": temp.temperature};
            db.child("Temp Update").update({"Current": temp.temperature});
            db.child(" Temperature Status").push(test,user['idToken']);
            
            test1={"Time" : x, "Humidity": temp.humidity};
            db.child("Humidity Update").update({"Current": temp.humidity});
            db.child(" Humidity Status").push(test1,user['idToken']);
            time.sleep(20);
            
