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
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
# from ev3dev2.motor import SpeedPercent
# Initialize the color sensor
cs = ColorSensor(Port.S4)

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize two motors with default settings on Port B and Port C.
# These will be the left and right motors of the drive base.

medium_motor = Motor(Port.A)
# The DriveBase is composed of two motors, with a wheel on each motor.
# The wheel_diameter and axle_track values are used to make the motors
# move at the correct speed when you give a motor command.
# The axle track is the distance between the points where the wheels
# touch the ground.


# Play a sound to tell us when we are ready to start moving
ev3.speaker.beep()

# The following loop makes the robot drive forward until it detects an
# obstacle. Then it backs up and turns around. It keeps on doing this
# until you stop the program.
while True:

    color = cs.color()
    print("Detected Color: " + str(color))

    # If green is detected, take action
    if str(color) == "Color.YELLOW":
        print("Yellow...Counterclockwise!")
        medium_motor.run_angle(500, 360)

    wait(1000)

    if str(color) == "Color.RED":
        print("Red...Faster counterclockwise!")
        medium_motor.run_angle(500, 360)  # 500 deg/s speed, 360 degrees rotation
    wait(1000)  # Wait for 1 second


   


