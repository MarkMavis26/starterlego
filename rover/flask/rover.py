# Install dependencies:
# pip install -r requirements.txt
# Execute flask:
# flask --app rover run --host=0.0.0.0 --port=5001 --debug

from flask import Flask, jsonify, request, render_template
from bokeh.plotting import figure, show
from bokeh.embed import components
from flask_sqlalchemy import SQLAlchemy

import math
import json
import random

app = Flask(__name__)

# Initialize our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# Define the Mission model
class Mission(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement
    name = db.Column(db.String(100), nullable=False)
    x_coord = db.Column(db.Integer, default=0)
    y_coord = db.Column(db.Integer, default=0)

    # Specify foreign keys explicitly in the relationship
    telemetry = db.relationship(
        'Telemetry',
        backref='mission',
        lazy=True,
        foreign_keys='Telemetry.mission_id'  # Use the correct foreign key column
    )

    def __repr__(self):
        return f'<Mission {self.name}>'

# Define the Telemetry model
class Telemetry(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement
    sensor_distance = db.Column(db.Float, default=0)
    distance_in_centimeters = db.Column(db.Float, default=random.random)
    wheel_rotation_angle = db.Column(db.Integer, default=0)
    current_robot_angle = db.Column(db.Integer, default=random.randint(1, 360))
    x_coord = db.Column(db.Integer, db.ForeignKey('mission.x_coord'))
    y_coord = db.Column(db.Integer, db.ForeignKey('mission.y_coord'))
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))  # Explicit foreign key

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

def process_telemetry(mission, telemetry_data):
  
    distance_in_centimeters = telemetry_data['distance_in_centimeters']
    current_robot_angle = math.radians(telemetry_data['current_robot_angle'])
    mission['x_coord'] = mission['x_coord'] + (math.cos(current_robot_angle) * distance_in_centimeters)
    mission['y_coord'] = mission['y_coord'] + (math.sin(current_robot_angle) * distance_in_centimeters)
    telemetry_data['x_coord'] = mission['x_coord']
    telemetry_data['y_coord'] = mission['y_coord']

    
@app.route('/missions', methods=['GET'])
def get_missions():
    """List all missions."""
    # Query all missions from the database
    missions = Mission.query.all()
    return jsonify([mission.as_dict() for mission in missions]), 200

@app.route('/missions/<int:id>', methods=['GET'])
def get_mission(id):
    """Retrieve details about a particular mission."""
    # Query the database for the mission by id
    mission = Mission.query.get(id)
    if mission:
        return jsonify(mission.as_dict()), 200
    return jsonify({"error": "Mission not found"}), 404

@app.route('/missions', methods=['POST'])
def create_mission():
    """Create a new mission."""
    mission_data = request.get_json()
    
    # Create a new Mission instance
    new_mission = Mission(
        name=mission_data.get('name', generate_robot_mission_name()),
        x_coord=mission_data.get('x_coord', 0),
        y_coord=mission_data.get('y_coord', 0),
    )
    
    # Add the mission to the database session
    db.session.add(new_mission)
    db.session.commit()  # Commit to persist changes to the database

    return jsonify({"id": new_mission.id}), 201

@app.route('/missions/<int:id>/telemetry', methods=['POST'])
def create_mission_telemetry(id):
    """Send telemetry packet to a mission."""
    # Check if the mission exists in the database
    mission = Mission.query.get(id)
    if not mission:
        return jsonify({"error": "Mission not found"}), 404

    telemetry_data = request.get_json()

    # Extract the telemetry processing logic into a reusable function
    process_telemetry(mission, telemetry_data)

    # Create and save a new telemetry record in the database
    new_telemetry = Telemetry(
        mission_id=mission.id,
        sensor_distance=telemetry_data.get("sensor_distance", 0),
        distance_in_centimeters=telemetry_data.get("distance_in_centimeters", 0),
        wheel_rotation_angle=telemetry_data.get("wheel_rotation_angle", 0),
        current_robot_angle=telemetry_data.get("current_robot_angle", 0),
        x_coord=telemetry_data.get("x_coord", mission.x_coord),
        y_coord=telemetry_data.get("y_coord", mission.y_coord),
    )
    db.session.add(new_telemetry)
    db.session.commit()

    return jsonify({"message": "Telemetry received"}), 200

@app.route('/missions/<int:id>/telemetry', methods=['GET'])
def list_telemetry(id):
    """List all telemetry for a given mission."""
    # Check if the mission exists in the database
    mission = Mission.query.get(id)
    if not mission:
        return jsonify({"error": "Mission not found"}), 404

    # Retrieve all telemetry records for the mission
    mission_telemetry = Telemetry.query.filter_by(mission_id=id).all()

    # Use BaseModel's as_dict() for serialization
    telemetry_list = [telemetry.as_dict() for telemetry in mission_telemetry]

    return jsonify({"telemetry": telemetry_list}), 200

#UI Below
@app.route('/ui/missions/<int:id>')
def mission_telemetry(id):
    # Retrieve the mission from the database
    mission = Mission.query.get(id)
    if not mission:
        return render_template('telemetry.html', mission_name="Unknown Mission", script="", div="")

    # Retrieve telemetry data for the mission
    mission_name = mission.name
    mission_telemetry = Telemetry.query.filter_by(mission_id=mission.id).all()

    # Extract coordinates
    x_coords = [t.x_coord for t in mission_telemetry]
    y_coords = [t.y_coord for t in mission_telemetry]

    # Create a Bokeh plot with Cartesian coordinates
    plot = figure(title=f"Telemetry for {mission_name}", x_axis_label="X", y_axis_label="Y")
    plot.circle(x_coords, y_coords, size=10, color="blue", legend_label="Telemetry Points")

    # Embed the plot into the page
    script, div = components(plot)

    return render_template('telemetry.html', mission_name=mission_name, script=script, div=div)

@app.route('/ui/missions', methods=['GET'])
def home():
    # Retrieve all missions from the database
    all_missions = Mission.query.all()
    return render_template('index.html', missions=[mission.as_dict() for mission in all_missions])

def seed_data():
    print("Seeding data")

    # Check if data already exists
    if Mission.query.count() > 0:
        print("Data already exists. Skipping seeding.")
        return

    # Create sample missions
    for mission_id in range(1):
        mission = Mission(
            name=f"Mission {mission_id + 1}",
            x_coord=0,
            y_coord=0
        )
        db.session.add(mission)
        db.session.commit()  # Commit here to get mission.id for telemetry

        # Create sample telemetry
        for _ in range(10):
            telemetry_data = Telemetry(
                mission_id=mission.id,
                sensor_distance=0,
                distance_in_centimeters=random.uniform(0, 100),  # Random distance
                wheel_rotation_angle=random.randint(0, 360),      # Random angle 0-360
                current_robot_angle=random.randint(0, 360),       # Random angle 0-360
                x_coord=random.randint(-100, 100),                # Random x coord
                y_coord=random.randint(-100, 100)                 # Random y coord
            )
            db.session.add(telemetry_data)

    # Commit all telemetry records
    db.session.commit()
    print("Seeding complete.")

# Create the database and tables
with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
