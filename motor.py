# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
import socket
from adafruit_motorkit import MotorKit
import adafruit_hcsr04

# frontsonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

# motor1: left motor
# motor2: right motor
kit = MotorKit(i2c=board.I2C())

# s = socket.socket()
# host = ""
# port = 12345
# s.bind((host, port))
# s.listen(5)

# while True:
#     # try:
#     #     clientsock, addr = s.accept()
#     # except OSError:
#     #     continue
#     # message = clientsock.recv(20)
#     try:
#         print((frontsonar.distance))
#     except RuntimeError:
#         print("Retry")
#     time.sleep(0.1)

    # if(message=="forward" and frontsonar.distance > 5):
    #     kit.motor1.throttle = 0.8
    #     kit.motor2.throttle = 0.8
    # elif(message=="leftward"):
    #     kit.motor1.throttle = -0.8
    #     kit.motor2.throttle = 0.8
    # elif(message=="rightward"):
    #     kit.motor1.throttle = 0.8
    #     kit.motor2.throttle = -0.8
    # elif(message=="backward"):
    #     kit.motor1.throttle = -0.8
    #     kit.motor2.throttle = -0.8

#testing motors

while True:
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = -1.0