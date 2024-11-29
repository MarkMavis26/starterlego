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


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
)



left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
#tank_drive = MoveTank(Port.A, Port.B)
color_sensor = ColorSensor(Port.S3)

#function controls steering
#def move_steering(steering, speed, duration):
    #left_speed = speed + (steering / 100) * speed
    #right_speed = speed - (steering / 100) * speed

   # wait(duration * 1000)

  #  left_motor.stop()
 #   right_motor.stop()

#move_steering(steering=0, speed=500, duration=2)

TARGET_LIGHT_INTENSITY = 50  # Adjust based on your setup (midway between black and white)
KP = 2.0                    # Proportional gain (tune this value for better performance)
BASE_SPEED = 75            # Base speed of the robot (in degrees per second)

def follow_line():
    while True:
        # Read reflected light intensity
        light_intensity = color_sensor.reflection()
        
        # Calculate error
        error = TARGET_LIGHT_INTENSITY - light_intensity
        
        # Calculate adjustment using proportional control
        turn_rate = KP * error

        # Adjust motor speeds
        left_speed = BASE_SPEED + turn_rate
        right_speed = BASE_SPEED - turn_rate

        # Apply motor speeds
        left_motor.run(left_speed)
        right_motor.run(right_speed)

        # Log important variables
        logging.info("Light Intensity: {}".format(light_intensity))
        logging.info("Error: {}".format(error))
        logging.info("Turn Rate: {}".format(turn_rate))

        # Log motor speeds
        logging.info("Left Speed: {}".format(left_speed))
        logging.info("Right Speed: {}".format(right_speed))

        
        # Small delay for smoother control
        wait(10)

# Run the program
if __name__ == "__main__":
    try:
        follow_line()
    except:
        # Stop motors when exiting
        left_motor.stop()
        right_motor.stop()




   


