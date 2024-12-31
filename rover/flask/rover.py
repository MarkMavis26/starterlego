from flask import Flask, jsonify, request

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
    mission_data['id'] = current_mission_id
    missions[current_mission_id] = mission_data
    current_mission_id += 1
    return jsonify({"id": mission_data['id']}), 201

@app.route('/missions/<int:id>/telemetry', methods=['POST'])
def send_telemetry(id):
    """Send telemetry packet to a mission."""
    if id not in missions:
        return jsonify({"error": "Mission not found"}), 404
    
    telemetry_data = request.get_json()
    if id not in telemetry:
        telemetry[id] = []
    
    telemetry[id].append(telemetry_data)
    return jsonify({"message": "Telemetry received"}), 200

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

if __name__ == '__main__':
    app.run(debug=True)
