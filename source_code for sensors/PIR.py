import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
GPIO. setup(24, GPIO.OUT)


while True:
    if GPIO.input(23):
        GPIO.output(24, True)
        time.sleep(0.5)
        GPIO.output(24,False)
        print("Motion Detected")
        state="motion detected"
        time.sleep(2)








