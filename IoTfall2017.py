import RPi.GPIO as GPIO
import time
import pyrebase
from datetime import datetime
import dht11
import threading 

#configuring firebase

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

#Initilializing GPIO board for inputs and outputs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)
GPIO. setup(24, GPIO.OUT)
instance=dht11.DHT11(pin=6)
temp=instance.read()
door=0;
pin_to_circuit=4;
def temp_sensor(): #function to calculate temperatyre and humidity
    global temp;
    if temp.is_valid(): 
            x=str(datetime.now());
            test={"Time" : x, "Temperature": str(temp.temperature)};
            db.child("Temp Update").update({"Current": temp.temperature});
            db.child(" Temperature Status").push(test,user['idToken']);
            
            test1={"Time" : x, "Humidity": str(temp.humidity)};
            db.child("Humidity Update").update({"Current": temp.humidity});
            db.child(" Humidity Status").push(test1,user['idToken']);
            time.sleep(30);
            
    
def door_sensor(channel): #function to find  door status
    global door;
    if GPIO.input(16)==0 and door==0:
            door=1;
            x=str(datetime.now())
            test={"Time": x, "Sensor": "Door open"}
            db.child("Status Door").update({"Current": "Opened"})
            db.child("Door").push(test, user['idToken'])
            print("door opened")
            time.sleep(0.2)
    elif GPIO.input(16)==0 and door==1:
            door=0;
            x=str(datetime.now())
            test={"Time": x, "Sensor": "Door close"}
            db.child("Status Door").update({"Current": "closed"})
            db.child("Door").push(test, user['idToken'])
            print("door closed")
            time.sleep(0.2)
def motion_detection(channel): #function to find motion detection
    if GPIO.input(23):
            GPIO.output(24,True)
            time.sleep(0.5)
            GPIO.output(24,False)
            x=str(datetime.now())
            test={"Time": x, "Sensor": "Motion Detected"}
            db.child("Motion Detection Update").update({"Current": "Motion Detected"})
            db.child("Motion Detection").push(test, user['idToken'])
            print("Motion Detected")
            time.sleep(2)
def motion_detection_1():
            db.child("Motion Detection Update").update({"Current": "Not Detected"})
            print("Motion not Detected")
            time.sleep(2)
def rc_time(pin_to_circuit): 
    count = 0;
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT);
    GPIO.output(pin_to_circuit, GPIO.LOW);
    time.sleep(0.1);

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN);
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count;
def light_sensor():  #function to calculate brightness based on a specific range of values
    if rc_time(pin_to_circuit) > 300:
            x=str(datetime.now())
            test={"Time": x, "Light": "Dark"}
            db.child("Light Status").update({"Current": "Dark"})
            db.child("Light Sensor").push(test, user['idToken'])
            print("Dark")
            time.sleep(30)
           
    else:
            x=str(datetime.now())
            test={"Time": x, "Light": "Bright"}
            db.child("Light Status").update({"Current": "Bright"})
            db.child("Light Sensor").push(test, user['idToken'])
            print("Bright")
            time.sleep(30)        
    

#main function to call all the functions in an infinite loop    
if __name__ == "__main__":
    try: #two interrupts to detect door status and motion
        GPIO.add_event_detect(16, GPIO.FALLING, callback=door_sensor)
        GPIO.add_event_detect(23, GPIO.BOTH, callback=motion_detection)
        while True:
            temp_sensor();
            light_sensor();
            motion_detection_1();
    except:
        GPIO.cleanup();
                             
