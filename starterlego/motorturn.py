#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Ultrasonic Sensor Driving Base Program
-----------------------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase

ev3 = EV3Brick()



left_motor = Motor(Port.B)
right_motor = Motor(Port.C)


#function controls steering
def move_steering(steering, speed, duration):
    left_speed = speed + (steering / 100) * speed
    right_speed = speed - (steering / 100) * speed

    wait(duration * 1000)

    left_motor.stop()
    right_motor.stop()

move_steering(steering=0, speed=500, duration=2)






   


