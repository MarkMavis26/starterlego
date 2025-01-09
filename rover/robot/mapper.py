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
import urequests
import ujson

ev3 = EV3Brick()
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
)
print("debug 1")
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S2)

def move(m: Motor, s: int, r: int, w: bool):
    m.run_angle(speed=s, rotation_angle=r, wait=w)

def forward(rot_angle_cm: int):
    move(left_motor, 200, rot_angle_cm, False)    
    move(right_motor, 200, rot_angle_cm, True)   

def pivot_right(rotation_angle: int): 
    move(left_motor, 200, rotation_angle, False)    
    move(right_motor, 200, -rotation_angle, True)
    #todo: confirm rotation angle    
    (rotation_angle/500)*90

def pivot_left(rotation_angle: int):
    move(right_motor, 200, rotation_angle, False)    
    move(left_motor, 200, -rotation_angle, True)
    #todo: confirm rotation angle    
    -(rotation_angle/500)*90

def backward(rot_angle_cm: int): 
    forward(-rot_angle_cm)

def send_telemetry(distance_in_centimeters, rot_angle_cm, current_angle, moved_cm):
    try:
        telemetry_data = {
            "distance_in_cm": distance_in_centimeters,
            "move_rot": rot_angle_cm,
            "current_angle": current_angle,
            "moved_cm": moved_cm
        }
        print(ujson.dumps(telemetry_data))
        telemetry_response = urequests.post("{}/missions/{}/telemetry".format(server, missionID), json=telemetry_data, headers=headers)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)       

    
def main():
    targ = range(10,100000)
    rot_angle_cm=31.83098863
    #each rotation moves the bot forward approx 5cm
    print("debug 3")
   
    server = "http://192.168.4.69:5001"
    print("debug 4")
    #create mission against flask server
    headers = {'Content-Type': 'application/json'}
    print("debug 4")
    payload = ujson.dumps({})
    print("debug 4")
    #https://www.ev3dev.org/docs/tutorials/setting-up-wifi-using-the-command-line/
    r = urequests.post("{}/missions".format(server), data=payload, headers=headers)
    print("debug 5")
    # missionID = r.json()['id']
    
    response_data = r.json()
    missionID = response_data['id']
    print("Response:", response_data)
    print("Mission ID:", missionID) 
  
    # logging.info("response: {}, missionID: {}".format(r.content, missionID))
    current_angle = 0
    print("debug 6")
    #breakpoint()
    
    while True:
        forward(rot_angle_cm)
        distance_in_centimeters = ultrasonic_sensor.distance()/10
        logging.info("Distance: {} cm".format(distance_in_centimeters))
        print("debug 3")
        send_telemetry(distance_in_centimeters, rot_angle_cm, current_angle, 1)
       
       #IF LAST MEASURE LESS THAN 200 AND NEXT MEASURE IS GREATER THAN 2000, ASSUME YOU'VE HIT A WALL

        while distance_in_centimeters not in targ:
            backward(rot_angle_cm)
            send_telemetry(distance_in_centimeters, rot_angle_cm, current_angle, -1)

            wheel_rotation_angle=500
            logging.info("pivoting right {}".format(wheel_rotation_angle))

            current_angle+=pivot_right(wheel_rotation_angle)
            
            distance_in_centimeters = ultrasonic_sensor.distance()
        
if __name__ == "__main__":
    try:
        main()
    except:
        # Stop motors when exiting
        left_motor.stop()
        right_motor.stop()




   


