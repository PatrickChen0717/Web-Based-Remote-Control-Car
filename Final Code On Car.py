import time
import board
import socket
import pwmio
from adafruit_motorkit import MotorKit
import adafruit_hcsr04
from adafruit_motor import servo
import requests
import json
import base64
from picamera import PiCamera
import RPi.GPIO as GPIO

camera = PiCamera()

backsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
rightsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D13, echo_pin=board.D25)
leftsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D16, echo_pin=board.D19)
frontsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D20, echo_pin=board.D21)
pwm1 = pwmio.PWMOut(board.D23, frequency=50)
pwm2 = pwmio.PWMOut(board.D24, frequency=50)
topservo = servo.Servo(pwm1)
botservo = servo.Servo(pwm2)
topservo.angle = 90
botservo.angle = 90
# motor4: left motor
# motor2: right motor
kit = MotorKit(i2c=board.I2C())

shot = False

# These variables are for saving the data for runtime error case
frontdist=0
backdist=0
leftdist=0
rightdist=0
topangle = 0
botangle = 0
photostring=""

print("start")

while True:
    user_instruction=str()

    # Round the distance to one decimal places
    roundfront=round(frontdist,1)
    roundback=round(backdist,1)
    roundleft=round(leftdist,1)
    roundright=round(rightdist,1)
    
    # Build the json object for posting data to server
    newdata = {"leftdist": roundleft, "rightdist": roundright, "frontdist": roundfront, "backdist": roundback}
    newdataforimg={"image":""} # Seperate the empty image from distance data

    # Send the data to the server
    post1 = requests.post('http://cpen291-14.ece.ubc.ca/postdata', json=newdata)
    post2 = requests.post('http://cpen291-14.ece.ubc.ca/postimg', json=newdataforimg)

    # Send the image taken last time to server, this is only done when there is a new img to upload to save time
    if shot:
        newdata = {"leftdist": roundleft, "rightdist": roundright, "frontdist": roundfront, "backdist": roundback} # this is the new data sending to the server 
        newdataforimg = {"image":photostring}
        post1 = requests.post('http://cpen291-14.ece.ubc.ca/postdata', json=newdata)
        post2 = requests.post('http://cpen291-14.ece.ubc.ca/postimg', json=newdataforimg)
        time.sleep(1)
        shot = False

    get = requests.get('http://cpen291-14.ece.ubc.ca/getdata') # GET request 
    data = get.json() # Transform the data to json format

    # Set the two DC motors in correct direction to move in four directions
    if(data["direction"]=="forward"):
        kit.motor2.throttle = -1
        kit.motor4.throttle = 1
    elif(data["direction"]=="leftward"):
        kit.motor2.throttle = -1
        kit.motor4.throttle = -1
    elif(data["direction"]=="rightward"):
        kit.motor2.throttle = 1
        kit.motor4.throttle = 1
    elif(data["direction"]=="backward"):
        kit.motor2.throttle = 1
        kit.motor4.throttle = -1
    else: # In this case the motors will stop
        kit.motor2.throttle = 0
        kit.motor4.throttle = 0
    
    try:
        # Get the sonar sensor data and store them for runtimeerror case
        frontdist=frontsonar.distance
        backdist=backsonar.distance
        leftdist=leftsonar.distance
        rightdist=rightsonar.distance

        # Section for auto photo taking while within warning distance
        if(rightdist<=10 and rightdist > 1):
            # Auto stop the car
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0

            # Rotate the servos to correct angle
            topservo.angle = 180
            botservo.angle = 180
            topangle = 180
            botangle = 180

            # Setup the camera and take a shot
            camera.resolution = (1920, 1080)
            time.sleep(0.5)
            camera.capture('/home/pi/my_photo.jpg')
            with open("/home/pi/my_photo.jpg","rb") as img_file:
                photostring=base64.b64encode(img_file.read())
            shot = True

            # Set the motor in the reverse direction to avoid the obstacle
            kit.motor2.throttle = -1
            kit.motor4.throttle = -1
            time.sleep(0.6)
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0
            
        elif(leftdist<=10 and leftdist > 1):
            # Auto stop the car
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0

            # Rotate the servos to correct angle
            topservo.angle = 80
            botservo.angle = 80
            topangle = 80
            botangle = 80

            # Setup the camera and take a shot
            camera.resolution = (1920, 1080)
            time.sleep(0.5)
            camera.capture('/home/pi/my_photo.jpg')
            with open("/home/pi/my_photo.jpg","rb") as img_file:
                photostring=base64.b64encode(img_file.read())
            shot = True

            # Set the motor in the reverse direction to avoid the obstacle
            kit.motor2.throttle = 1
            kit.motor4.throttle = 1
            time.sleep(0.6)
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0
            
        elif(backdist<=10 and backdist > 1):
            # Auto stop the car
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0

            # Rotate the servos to correct angle
            topservo.angle = 130
            botservo.angle = 130
            topangle = 130
            botangle = 130

            # Setup the camera and take a shot
            camera.resolution = (1920, 1080)
            time.sleep(0.5)
            camera.capture('/home/pi/my_photo.jpg')
            with open("/home/pi/my_photo.jpg","rb") as img_file:
                photostring=base64.b64encode(img_file.read())
            shot = True

            # Set the motor in the reverse direction to avoid the obstacle
            kit.motor2.throttle = -1
            kit.motor4.throttle = 1
            time.sleep(0.6)
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0
        
        elif(frontdist<=10 and frontdist > 1):
            # Auto stop the car
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0

            # Rotate the servos to correct angle
            topservo.angle = 0
            botservo.angle = 0
            topangle = 0
            botangle = 0

            # Setup the camera and take a shot
            camera.resolution = (1920, 1080)
            time.sleep(0.5)
            camera.capture('/home/pi/my_photo.jpg')
            with open("/home/pi/my_photo.jpg","rb") as img_file:
                photostring=base64.b64encode(img_file.read())
            shot = True

            # Set the motor in the reverse direction to avoid the obstacle
            kit.motor2.throttle = 1
            kit.motor4.throttle = -1
            time.sleep(0.6)
            kit.motor2.throttle = 0
            kit.motor4.throttle = 0
        
        else: # Other case that the camera does not need to take a shot
            topservo.angle = 0
            botservo.angle = 0
            topangle = 0
            botangle = 0
            photostring=""

    except RuntimeError:
        topservo.angle = topangle
        botservo.angle = botangle
