from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath): return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return []

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_next_id(data):
    return max([item.get('id', 0) for item in data] + [0]) + 1

@app.route("/", methods=['GET'])
def api_home():
    return jsonify({"status": "API Online", "endpoints": ["/config/lb", "/config/ws", "/config/rp"]})

# Routes génériques pour LB, WS, RP
@app.route("/config/<type>", methods=['GET', 'POST'])
def manage_list(type):
    file = f"{'loadbalancer' if type=='lb' else 'webserver' if type=='ws' else 'reverseproxy'}.json"
    data = load_data(file)
    if request.method == 'POST':
        new_item = request.json
        new_item['id'] = get_next_id(data)
        data.append(new_item)
        save_data(file, data)
        return jsonify(new_item), 201
    return jsonify(data)

@app.route("/config/<type>/<int:id>", methods=['GET', 'DELETE'])
def manage_item(type, id):
    file = f"{'loadbalancer' if type=='lb' else 'webserver' if type=='ws' else 'reverseproxy'}.json"
    data = load_data(file)
    if request.method == 'DELETE':
        new_data = [i for i in data if i.get('id') != id]
        save_data(file, new_data)
        return jsonify({"success": True})
    item = next((i for i in data if i.get('id') == id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True, port=5001)