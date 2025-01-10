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
from pybricks.parameters import Port
from pybricks.nxtdevices import UltrasonicSensor
import logging
import urequests
import ujson
import random

# instantiate ev3 objects representing bricks, motors, sensors, etc
ev3 = EV3Brick()
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S2)

# global variables
default_motor_rotation_speed = 200
rotation_degrees_per_centimeter = 31.83098863

# networking variables
server = "http://192.168.4.69:5001"
headers = {'Content-Type': 'application/json'}

# private functions

# robot movement/sensor
def move(m: Motor, s: int, r: int, w: bool):
    m.run_angle(speed=s, rotation_angle=r, wait=w)

def forward(distance_in_centimeters: int):
    rotation_angle = distance_in_centimeters * rotation_degrees_per_centimeter
    move(left_motor, default_motor_rotation_speed, rotation_angle, False)    
    move(right_motor, default_motor_rotation_speed, rotation_angle, True)   

def backward(distance_in_centimeters: int): 
    forward(-distance_in_centimeters)

def pivot_right(rotation_angle: int): 
    wheel_rotation_angle = rotation_angle_to_wheel_rotation_angle(rotation_angle)
    move(left_motor, default_motor_rotation_speed, wheel_rotation_angle, False)    
    move(right_motor, default_motor_rotation_speed, -wheel_rotation_angle, True)

def pivot_left(rotation_angle: int):
    wheel_rotation_angle = -rotation_angle_to_wheel_rotation_angle(rotation_angle)
    move(right_motor, default_motor_rotation_speed, wheel_rotation_angle, False)    
    move(left_motor, default_motor_rotation_speed, -wheel_rotation_angle, True)

def calculate_sensor_distance_centimeters():
    return ultrasonic_sensor.distance()/10

# calculation functions
def rotation_angle_to_robot_distance_cm(rotation_angle: int):
    return rotation_angle/rotation_degrees_per_centimeter

def rotation_angle_to_wheel_rotation_angle(rotation_angle: int):
    return (rotation_angle / 90) * 500

def generate_robot_mission_name():
    # Dictionaries of wild adjectives, animals, and numbers
    adjectives = ["Zany", "Wild", "Crazy", "Bold", "Sassy", "Brave", "Sneaky", "Witty", "Funky", "Hyper"]
    animals = ["Panther", "Falcon", "Tiger", "Llama", "Cobra", "Penguin", "Gorilla", "Octopus", "Badger", "Chameleon"]
    numbers = list(range(1, 101))  # Numbers from 1 to 100

    # Randomly pick one from each category
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.choice(numbers)

    # Combine them into a zany mission name
    mission_name = "{} {} {}".format(adjective, animal, number)
    return mission_name

# rest client calls
def send_telemetry(mission_id, sensor_distance, wheel_rotation_angle, current_robot_angle, distance_in_centimeters):
    telemetry_data = {
        "sensor_distance": sensor_distance,
        "wheel_rotation_angle": wheel_rotation_angle,
        "current_robot_angle": current_robot_angle,
        "distance_in_centimeters": distance_in_centimeters
    }
    # print(ujson.dumps(telemetry_data))
    urequests.post("{}/missions/{}/telemetry".format(server, mission_id), json=telemetry_data, headers=headers)
    
def main():
    targ = range(10,100000)
    
    # networking setup:
    # https://www.ev3dev.org/docs/tutorials/setting-up-wifi-using-the-command-line/

    # initialize mission
    payload = ujson.dumps({ "name": generate_robot_mission_name() })
    r = urequests.post("{}/missions".format(server), data=payload, headers=headers)    
    response_data = r.json()
    mission_id = response_data['id']
    print("Response:", response_data)
    print("Mission ID:", mission_id) 
  
    # current direction the rover is pointed
    current_robot_angle = 0

    # breakpoint()
    
    move_distance_centimeters = 1
    correction_right_angle = 90
    rotation_angle_per_move = rotation_degrees_per_centimeter * move_distance_centimeters

    while True:

        forward(move_distance_centimeters)

        # distance() returns mm, we convert to cm
        sensor_distance_centimeters = calculate_sensor_distance_centimeters()
        logging.info("Distance: {} cm".format(sensor_distance_centimeters))

        send_telemetry(mission_id, sensor_distance_centimeters, rotation_angle_per_move, current_robot_angle, move_distance_centimeters)
       
        while sensor_distance_centimeters not in targ:
            backward(move_distance_centimeters)
            send_telemetry(mission_id, sensor_distance_centimeters, rotation_angle_per_move, current_robot_angle, -move_distance_centimeters)

            logging.info("pivoting right {} degrees".format(correction_right_angle))

            pivot_right(correction_right_angle)
            current_robot_angle += correction_right_angle
            
            sensor_distance_centimeters = calculate_sensor_distance_centimeters()
        
if __name__ == "__main__":
    try:
        main()
    except:
        # Stop motors when exiting
        left_motor.stop()
        right_motor.stop()