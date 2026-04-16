from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/")
def hello():
    return "Hello, l'API fonctionne !"

@app.route("/config/lb", methods=['GET'])
def get_lb_list():
    donnees = load_data('loadbalancer.json')
    return jsonify(donnees)

if __name__ == '__main__':
    app.run(debug=True, port=5001)