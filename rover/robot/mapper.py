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
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.nxtdevices import UltrasonicSensor
import logging

ev3 = EV3Brick()
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
)
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S1)

def move(m: Motor, s: int, r: int, w: bool):
    m.run_angle(speed=s, rotation_angle=r, wait=w)

def forward(rot_angle_cm: int):
    move(left_motor, 200, rot_angle_cm, False)    
    move(right_motor, 200, rot_angle_cm, True)   

def pivot_right(move_angle: int): 
    move(left_motor, 200, move_angle, False)    
    move(right_motor, 200, -move_angle, True)    

def pivot_left(move_angle: int):
    move(right_motor, 200, move_angle, False)    
    move(left_motor, 200, -move_angle, True)

def backward(rot_angle_cm: int): 
    forward(-rot_angle_cm)

def main():
    targ = range(10,100000)
    rot_angle_cm=31.83098863
    #each rotation moves the bot forward approx 5cm
    move_angle=500

    while True:
        forward(rot_angle_cm)
        distance_in_centimeters = ultrasonic_sensor.distance()/10
        logging.info("Distance: {} cm".format(distance_in_centimeters))
       #IF LAST MEASURE LESS THAN 200 AND NEXT MEASURE IS GREATER THAN 2000, ASSUME YOU'VE HIT A WALL
        while distance_in_centimeters not in targ:
            backward(rot_angle_cm)
            logging.info("pivoting right {}".format(move_angle))
            pivot_right(move_angle)
            distance_in_centimeters = ultrasonic_sensor.distance()
        
if __name__ == "__main__":
    try:
        main()
    except:
        # Stop motors when exiting
        left_motor.stop()
        right_motor.stop()




   


