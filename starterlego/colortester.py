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
import logging

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C) 
#tank_drive = MoveTank(Port.A, Port.B)
color_sensor = ColorSensor(Port.S3)

def test_color():
    while True:
        light_intensity = color_sensor.reflection()

        logging.info("Light Intensity: {}".format(light_intensity))

if __name__ == "__main__":
    test_color()