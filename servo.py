# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
import socket
import pwmio
from adafruit_motorkit import MotorKit
import adafruit_hcsr04
from adafruit_motor import servo


frontsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
leftsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D13, echo_pin=board.D25)
rightsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D16, echo_pin=board.D19)
backsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D20, echo_pin=board.D21)
pwm1 = pwmio.PWMOut(board.D23, frequency=50)
pwm2 = pwmio.PWMOut(board.D24, frequency=50)
topservo = servo.Servo(pwm1)
botservo = servo.Servo(pwm2)
topservo.angle = 90
botservo.angle = 90
# motor1: left motor
# motor2: right motor
# kit = MotorKit(i2c=board.I2C())

# s = socket.socket()
# host = ""
# port = 12345
# s.bind((host, port))
# s.listen(5)

# while True:
#     try:
#         clientsock, addr = s.accept()
#     except OSError:
#         continue
#     message = clientsock.recv(20)

#     if(message=="forward" and frontsonar.distance > 5):
#         kit.motor1.throttle = 0.8
#         kit.motor2.throttle = 0.8
#     elif(message=="leftward"):
#         kit.motor1.throttle = -0.8
#         kit.motor2.throttle = 0.8
#     elif(message=="rightward"):
#         kit.motor1.throttle = 0.8
#         kit.motor2.throttle = -0.8
#     elif(message=="backward"):
#         kit.motor1.throttle = -0.8
#         kit.motor2.throttle = -0.8

# #testing motors
# kit.motor1.throttle = 0.8
# kit.motor2.throttle = 0.8
# time.sleep(2)
# kit.motor1.throttle = -1.0
# kit.motor1.throttle = -1.0
# time.sleep(2)
# kit.motor1.throttle = 0
# kit.motor1.throttle = 0

while True:
    # topservo.angle = 90
    # botservo.angle = 90
    time.sleep(0.1)
    try:
        print("frontdistance: ",frontsonar.distance," leftdistance: ",leftsonar.distance, " rightdistance: ",rightsonar.distance," backdistance: ",backsonar.distance)
        if(rightsonar.distance<=10):
            print("right")
            topservo.angle = 180
            botservo.angle = 180
        elif(leftsonar.distance<=10):
            print("left")
            topservo.angle = 80
            botservo.angle = 80
        elif(backsonar.distance<=10):
            print("back")
            topservo.angle = 130
            botservo.angle = 130
        else:
            print("front")
            topservo.angle = 0
            botservo.angle = 0
            
    except RuntimeError:
        print("Retry!")

# while True:
#     topservo.angle = 90
#     for i in range(20):
#         topservo.angle += 1
    
#     for i in range(20):
#         topservo.angle -= 1
#     # topservo.angle = 180
    # time.sleep(3)
    # topservo.angle = 180