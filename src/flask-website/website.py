from flask import Flask, render_template, request, redirect, url_for, Response, session
import requests

app = Flask(__name__)
app.secret_key = "tp3_TRI" 
API_URL = "http://127.0.0.1:5001"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
            session['user'] = 'admin'
            return redirect(url_for('start'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('start'))

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/<type>/list")
def item_list(type):
    titles = {"lb": "Load Balancers", "ws": "Serveurs Web", "rp": "Reverse Proxies"}
    data = requests.get(f"{API_URL}/config/{type}").json()
    return render_template("list.html", items=data, title=titles[type], type=type)

@app.route("/<type>/create", methods=['GET', 'POST'])
def item_create(type):
    if not session.get('user'): return redirect(url_for('login'))
    if request.method == 'POST':
        data = {k: v for k, v in request.form.items()}
        requests.post(f"{API_URL}/config/{type}", json=data)
        return redirect(url_for('item_list', type=type))
    return render_template("create.html", type=type)

@app.route("/<type>/<int:id>")
def item_detail(type, id):
    item = requests.get(f"{API_URL}/config/{type}/{id}").json()
    return render_template("detail.html", item=item, type=type)

@app.route("/<type>/<int:id>/delete", methods=['POST'])
def item_delete(type, id):
    if not session.get('user'): return redirect(url_for('login'))
    requests.delete(f"{API_URL}/config/{type}/{id}")
    return redirect(url_for('item_list', type=type))

@app.route("/<type>/<int:id>/download")
def download(type, id):
    item = requests.get(f"{API_URL}/config/{type}/{id}").json()
    content = render_template(f"nginx_template.txt", item=item, type=type)
    return Response(content, mimetype="text/plain", 
                    headers={"Content-Disposition": f"attachment;filename={type}_{id}.conf"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)