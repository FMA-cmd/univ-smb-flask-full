from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_next_id(data):
    return max([item.get('id', 0) for item in data] + [0]) + 1

@app.route("/config/lb", methods=['GET'])
def get_lb_list(): return jsonify(load_data('loadbalancer.json'))

@app.route("/config/lb/<int:id>", methods=['GET'])
def get_lb_detail(id):
    donnees = load_data('loadbalancer.json')
    item = next((i for i in donnees if i.get('id') == id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route("/config/lb", methods=['POST'])
def create_lb():
    donnees = load_data('loadbalancer.json')
    nouveau = request.json
    nouveau['id'] = get_next_id(donnees)
    donnees.append(nouveau)
    save_data('loadbalancer.json', donnees)
    return jsonify(nouveau), 201

@app.route("/config/lb/<int:id>", methods=['DELETE'])
def delete_lb(id):
    donnees = load_data('loadbalancer.json')
    nouvelles_donnees = [item for item in donnees if item.get('id') != id]
    if len(donnees) != len(nouvelles_donnees):
        save_data('loadbalancer.json', nouvelles_donnees)
        return jsonify({"success": True}), 200
    return jsonify({"error": "Introuvable"}), 404

@app.route("/config/ws", methods=['GET'])
def get_ws_list(): return jsonify(load_data('webserver.json'))

@app.route("/config/ws/<int:id>", methods=['GET'])
def get_ws_detail(id):
    donnees = load_data('webserver.json')
    item = next((i for i in donnees if i.get('id') == id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route("/config/ws", methods=['POST'])
def create_ws():
    donnees = load_data('webserver.json')
    nouveau = request.json
    nouveau['id'] = get_next_id(donnees)
    donnees.append(nouveau)
    save_data('webserver.json', donnees)
    return jsonify(nouveau), 201

@app.route("/config/ws/<int:id>", methods=['DELETE'])
def delete_ws(id):
    donnees = load_data('webserver.json')
    nouvelles_donnees = [item for item in donnees if item.get('id') != id]
    if len(donnees) != len(nouvelles_donnees):
        save_data('webserver.json', nouvelles_donnees)
        return jsonify({"success": True}), 200
    return jsonify({"error": "Introuvable"}), 404

@app.route("/config/rp", methods=['GET'])
def get_rp_list(): return jsonify(load_data('reverseproxy.json'))

@app.route("/config/rp/<int:id>", methods=['GET'])
def get_rp_detail(id):
    donnees = load_data('reverseproxy.json')
    item = next((i for i in donnees if i.get('id') == id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route("/config/rp", methods=['POST'])
def create_rp():
    donnees = load_data('reverseproxy.json')
    nouveau = request.json
    nouveau['id'] = get_next_id(donnees)
    donnees.append(nouveau)
    save_data('reverseproxy.json', donnees)
    return jsonify(nouveau), 201

@app.route("/config/rp/<int:id>", methods=['DELETE'])
def delete_rp(id):
    donnees = load_data('reverseproxy.json')
    nouvelles_donnees = [item for item in donnees if item.get('id') != id]
    if len(donnees) != len(nouvelles_donnees):
        save_data('reverseproxy.json', nouvelles_donnees)
        return jsonify({"success": True}), 200
    return jsonify({"error": "Introuvable"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)