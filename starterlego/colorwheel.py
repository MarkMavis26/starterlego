#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait



# Initialize the color sensor
cs = ColorSensor(Port.S4)

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize our medium motor
medium_motor = Motor(Port.A)

# Play a sound to tell us when we are ready to start moving
ev3.speaker.beep()

from time import sleep

# we are using the command pattern below to map functions to colors

# Define actions as functions
def move_counter_clockwise(color: str):
    print(color + "...counter clockwise!")
    medium_motor.run_angle(500, 360)  # 500 deg/s speed, 360 degrees rotation

def move_clockwise(color: str):
    print(color + "...clockwise!")
    medium_motor.run_angle(700, 360)  # Adjust speed for faster rotation

def move_back_and_forth(color: str):
    print(color + "...move back and forth!!")

    medium_motor.run_angle(700, 360)

    medium_motor.run_angle(700, -360)

def step_forward_two_back(color: str, a: int):
    print(color + "...no progress!!")

    medium_motor.run_angle(700, a)

    medium_motor.rug_angle(700, -2(a))

      # Adjust speed for faster rotation

# Map colors to functions
color_action_map = {
    "Color.YELLOW": move_counter_clockwise,
    "Color.RED": move_clockwise,
    "Color.GREEN": move_back_and_forth,
    "Color.BLUE": step_forward_two_back,
}

# Check for color and execute the mapped action
def handle_color_action(color: str):
    action = color_action_map.get(color)  # Get the function from the map
    if action:
        action(color)  # Execute the function
    else:
        print(f"No action mapped for color: {color}")

# Loop until we stop program

a = 60
while True:
    color = cs.color()
    handle_color_action(str(color), a)


   


