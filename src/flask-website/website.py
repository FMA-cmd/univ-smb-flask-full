from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5001"

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/lb/list")
def lb_list():
    donnees_api = requests.get(f"{API_URL}/config/lb").json()
    return render_template("list.html", items=donnees_api, title="Load Balancers", type="lb")

@app.route("/lb/<int:id>")
def lb_detail(id):
    reponse = requests.get(f"{API_URL}/config/lb/{id}")
    if reponse.status_code == 404: return "Introuvable", 404
    return render_template("detail.html", item=reponse.json(), type="lb")

@app.route("/lb/create", methods=['GET', 'POST'])
def lb_create():
    if request.method == 'POST':
        data = {"name": request.form.get("name"), "ip_bind": request.form.get("ip_bind"), "pass": request.form.get("pass")}
        requests.post(f"{API_URL}/config/lb", json=data)
        return redirect(url_for('lb_list'))
    return render_template("create.html", title="Créer un Load Balancer", type="lb")

@app.route("/lb/<int:id>/delete", methods=['POST'])
def lb_delete(id):
    requests.delete(f"{API_URL}/config/lb/{id}")
    return redirect(url_for('lb_list'))

@app.route("/ws/list")
def ws_list():
    donnees_api = requests.get(f"{API_URL}/config/ws").json()
    return render_template("list.html", items=donnees_api, title="Serveurs Web", type="ws")

@app.route("/ws/<int:id>")
def ws_detail(id):
    reponse = requests.get(f"{API_URL}/config/ws/{id}")
    if reponse.status_code == 404: return "Introuvable", 404
    return render_template("detail.html", item=reponse.json(), type="ws")

@app.route("/ws/create", methods=['GET', 'POST'])
def ws_create():
    if request.method == 'POST':
        data = {"name": request.form.get("name"), "port": request.form.get("port"), "domain": request.form.get("domain")}
        requests.post(f"{API_URL}/config/ws", json=data)
        return redirect(url_for('ws_list'))
    return render_template("create.html", title="Créer un Serveur Web", type="ws")

@app.route("/ws/<int:id>/delete", methods=['POST'])
def ws_delete(id):
    requests.delete(f"{API_URL}/config/ws/{id}")
    return redirect(url_for('ws_list'))

@app.route("/rp/list")
def rp_list():
    donnees_api = requests.get(f"{API_URL}/config/rp").json()
    return render_template("list.html", items=donnees_api, title="Reverse Proxies", type="rp")

@app.route("/rp/<int:id>")
def rp_detail(id):
    reponse = requests.get(f"{API_URL}/config/rp/{id}")
    if reponse.status_code == 404: return "Introuvable", 404
    return render_template("detail.html", item=reponse.json(), type="rp")

@app.route("/rp/create", methods=['GET', 'POST'])
def rp_create():
    if request.method == 'POST':
        data = {"name": request.form.get("name"), "port": request.form.get("port"), "domain": request.form.get("domain")}
        requests.post(f"{API_URL}/config/rp", json=data)
        return redirect(url_for('rp_list'))
    return render_template("create.html", title="Créer un Reverse Proxy", type="rp")

@app.route("/rp/<int:id>/delete", methods=['POST'])
def rp_delete(id):
    requests.delete(f"{API_URL}/config/rp/{id}")
    return redirect(url_for('rp_list'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)