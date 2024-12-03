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



left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
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

TARGET_LIGHT_INTENSITY = 5  # Adjust based on your setup (midway between black and white)
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
        wait(500)

def move(m: Motor, s: int, r: int, w: bool):
    m.run_angle(speed=s, rotation_angle=r, wait=w)
    

# should go forward amount determined by parameter, and return color intensity detected at end
def forward(rot_angle: int):
    move(left_motor, 200, rot_angle, False)    
    move(right_motor, 200, rot_angle, True)    
# should determine if there is black tape slightly to the left (ie, spin counterclockwise)
def pivot_right(rot_angle: int): 
    move(left_motor, 200, rot_angle, False)    
    move(right_motor, 200, -rot_angle, True)    
    
# # should determine if there is black tape slightly to the right (ie, spin clockwise)
def pivot_left(rot_angle: int):
    move(right_motor, 200, rot_angle, False)    
    move(left_motor, 200, -rot_angle, True)

# # should go backward amount determined by parameter, and return color intensity detected at end
def backward(rot_angle: int): 
    forward(-rot_angle)

def main():
    # assum we're already on a line, go forward
    targ = range(0,11)
    rot_angle=50
    while True:

        # we assume here that we're on black

        # 1) forward one space
        forward(rot_angle)

        # 2) check color 
        #   - if black, we can keep going.
        #   - if NOT black...
        light_intensity = color_sensor.reflection()
        logging.info("invoking forward {}".format(rot_angle))
        logging.info("Light Intensity: {}".format(light_intensity))

        mult = 1
        while light_intensity not in targ:
        # 3) pivot right 1 step.  If black, we want to stay this direction
            local_rotation_angle = rot_angle * mult
            logging.info("pivoting right {}".format(local_rotation_angle))

            pivot_right(local_rotation_angle)
            light_intensity = color_sensor.reflection()
            logging.info("Light Intensity: {}".format(light_intensity))

            if light_intensity not in targ:
                logging.info("pivoting left {}".format(local_rotation_angle))
                pivot_left(local_rotation_angle)
                pivot_left(local_rotation_angle)
                light_intensity = color_sensor.reflection()
            if light_intensity not in targ:
                pivot_right(local_rotation_angle)
            mult = mult + 1

            

    # if we've gone off line, check left, then right for where line heads

    # once we find line, backup slightly

    # loop, going forward again

# Run the program
if __name__ == "__main__":
    try:
        main()
    except:
        # Stop motors when exiting
        left_motor.stop()
        right_motor.stop()




   


