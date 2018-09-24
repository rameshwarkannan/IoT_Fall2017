import RPi.GPIO as GPIO
import time
import pyrebase
from datetime import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin_to_circuit = 4


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


def rc_time(pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        if rc_time(pin_to_circuit) > 300:
            x=str(datetime.now())
            test={"Time": x, "Light": "Dark"}
            db.child("Light Status").update({"Current": "Dark"})
            db.child("Light Sensor").push(test, user['idToken'])
            print("Dark")
            time.sleep(20)
           
        else:
            x=str(datetime.now())
            test={"Time": x, "Light": "Bright"}
            db.child("Light Status").update({"Current": "Bright"})
            db.child("Light Sensor").push(test, user['idToken'])
            print("Bright")
            time.sleep(20)        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
