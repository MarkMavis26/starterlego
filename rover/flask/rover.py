#flask --app rover run --host=0.0.0.0 --port=5001 --debug

from flask import Flask, jsonify, request, render_template
from bokeh.plotting import figure, show
from bokeh.embed import components

import math
import json
import random
app = Flask(__name__)

# In-memory database (for simplicity)
missions = {}
telemetry = {}
current_mission_id = 1



@app.route('/missions', methods=['GET'])
def get_missions():
    """List all missions."""
    return jsonify(list(missions.values())), 200

@app.route('/missions/<int:id>', methods=['GET'])
def get_mission(id):
    """Retrieve details about a particular mission."""
    mission = missions.get(id)
    if mission:
        return jsonify(mission), 200
    return jsonify({"error": "Mission not found"}), 404

@app.route('/missions', methods=['POST'])
def create_mission():
    """Create a new mission."""
    global current_mission_id
    mission_data = request.get_json()
    
    # TODO - introduce Mission class
    #
    #   mission = new Mission(current_mission_id)
    #
    mission_data['id'] = current_mission_id
    mission_data['x_coord'] = 0
    mission_data['y_coord'] = 0

    missions[current_mission_id] = mission_data
    current_mission_id += 1

    return jsonify({"id": mission_data['id']}), 201

def process_telemetry(mission, telemetry_data):
  
    distance_in_centimeters = telemetry_data['distance_in_centimeters']
    current_robot_angle = math.radians(telemetry_data['current_robot_angle'])
    mission['x_coord'] = mission['x_coord'] + (math.cos(current_robot_angle) * distance_in_centimeters)
    mission['y_coord'] = mission['y_coord'] + (math.sin(current_robot_angle) * distance_in_centimeters)
    telemetry_data['x_coord'] = mission['x_coord']
    telemetry_data['y_coord'] = mission['y_coord']

@app.route('/missions/<int:id>/telemetry', methods=['POST'])
def send_telemetry(id):
    """Send telemetry packet to a mission."""
    if id not in missions:
        return jsonify({"error": "Mission not found"}), 404
    
    telemetry_data = request.get_json()
    if id not in telemetry:
        telemetry[id] = []

    # TODO - extract the code below into a function so we can use it here, AND from our seed_data function  
      
    mission = missions.get(id)
    process_telemetry(mission, telemetry_data)
    telemetry[id].append(telemetry_data)

    print("Missions")
    print(json.dumps(missions, indent=4))
    print("Telemetry")
    print(json.dumps(telemetry, indent=4))

    return jsonify({"message": "Telemetry received"}), 200


@app.route('/missions/<int:id>/telemetry', methods=['GET'])
def list_telemetry(id):
    """List all telemetry for a given mission."""
    if id not in missions:
        return jsonify({"error": "Mission not found"}), 404
    
    # Retrieve telemetry data for the mission
    mission_telemetry = telemetry.get(id, [])
    return jsonify({"telemetry": mission_telemetry}), 200


@app.route('/missions/<int:id>/instruction', methods=['GET'])
def get_instruction(id):
    """Get instruction for the rover for a specific mission."""
    if id not in missions:
        return jsonify({"error": "Mission not found"}), 404

    # In a real scenario, this would check for new instructions.
    instruction = {
        "instruction": "Move forward 1 meter"  # Example instruction
    }
    return jsonify(instruction), 200

#UI Below
@app.route('/ui/missions/<int:id>')
def mission_telemetry(id):
    if id not in telemetry:
        return render_template('telemetry.html', mission_name="Unknown Mission", script="", div="")
    
    mission_name = "test" #missions[id]["name"]
    print(json.dumps(telemetry[id], indent=4))
    coordinates = telemetry[id]
    x_coords = [c["x_coord"] for c in coordinates]
    y_coords = [c["y_coord"] for c in coordinates]

    # Create a Bokeh plot with Cartesian coordinates
    plot = figure(title=f"Telemetry for {mission_name}", x_axis_label="X", y_axis_label="Y")
    plot.circle(x_coords, y_coords, size=10, color="blue", legend_label="Telemetry Points")

    # return show(plot)

    # # Embed the plot into the page
    script, div = components(plot)

    return render_template('telemetry.html', mission_name=mission_name, script=script, div=div)

@app.route('/ui/missions', methods=['GET'])
def home():
    return render_template('index.html', missions=missions)

def seed_data():
    ("Seeding data")
    global current_mission_id
    for i in range(1):
        mission_data = {}

        mission_data['id'] = current_mission_id
        mission_data['name'] = "Mission {}".format(current_mission_id)
        mission_data['x_coord'] = 0 
        mission_data['y_coord'] = 0

        missions[current_mission_id] = mission_data
     

        # create sample telemetry
        # - add X number of telemetry records with randomized x/y coords (ask chat GPT how to generate random values)
        # - also randomize angle (same way, 0-360)
        telemetry[current_mission_id] = []
        for i in range(10):
            telemetry_data = {}
            telemetry_data['sensor_distance'] = 0
            telemetry_data['distance_in_centimeters'] = random.random()
            telemetry_data['wheel_rotation_angle'] = 0
            telemetry_data['current_robot_angle'] = random.randint(1, 360)
            process_telemetry(mission_data, telemetry_data)
            telemetry[current_mission_id].append(telemetry_data)
        current_mission_id += 1

seed_data()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
