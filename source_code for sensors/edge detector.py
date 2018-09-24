import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def my_callback(channel):  
    if GPIO.input(16):     # if port 25 == 1  
        print "Rising edge detected on 25"  
    else:                  # if port 25 != 1  
        print "Falling edge detected on 25"  



GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback)  
  
