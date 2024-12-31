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
from pybricks.nxtdevices import UltrasonicSensor
import logging

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C) 
#tank_drive = MoveTank(Port.A, Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S2)

def move(m: Motor, s: int, r: int, w: bool):
    m.run_angle(speed=s, rotation_angle=r, wait=w)

def pivot_right(move_angle: int): 
    move(left_motor, 200, move_angle, False)    
    move(right_motor, 200, -move_angle, True)    

def pivot_left(move_angle: int):
    move(right_motor, 200, move_angle, False)    
    move(left_motor, 200, -move_angle, True)

def forward(rot_angle: int):
    move(left_motor, 200, rot_angle, False)    
    move(right_motor, 200, rot_angle, True)   

def test_distance():
    move_angle=100

    while True:
        distance = ultrasonic_sensor.distance()
        forward(move_angle)
        wait(200000000000000)
        logging.info("Distance: {} cm".format(distance))

if __name__ == "__main__":
    test_distance()