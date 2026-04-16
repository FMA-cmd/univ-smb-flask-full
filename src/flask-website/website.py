from flask import Flask, render_template
import requests 

app = Flask(__name__)

API_URL = "http://127.0.0.1:5001"

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/lb/list")
def lb_list():
    reponse = requests.get(f"{API_URL}/config/lb")
    donnees_api = reponse.json() 
    return render_template("list.html", items=donnees_api, title="Load Balancers", type="lb")

@app.route("/lb/<int:id>")
def lb_detail(id):
    reponse = requests.get(f"{API_URL}/config/lb/{id}")
    if reponse.status_code == 404:
        return "Configuration introuvable", 404       
    donnees_api = reponse.json()
    return render_template("detail.html", item=donnees_api, type="lb")

if __name__ == '__main__':
    app.run(debug=True, port=5000)