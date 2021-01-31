from flask import Flask, render_template, request, redirect, url_for,jsonify, session 
import importlib
from hashlib import md5
mfp = importlib.import_module("scrape_mfp")

app = Flask(__name__)
app.secret_key = "a random string"

session = {}
@app.route('/', methods= ["GET"])
def index():
    if 'username' in session and 'data' in session:
        username = session['username']
        data = session['data']

        totals = { **data['totals'], **{'exercise': data['exercise']} }
        measurements = data['measurements']

        return render_template('index.html', username=username,
        data=data,
        totals = totals,
        measurements = measurements)
    else:
        return redirect(url_for('login'))
        
@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        if 'username' in session:
            status = "Already logged in"
            return redirect(url_for('index'))
        else:
            return render_template("login.html")
    else:
        result = request.form.get("master_password")
        status = mfp.login(result)
        if status == "":
            session['username'] = md5('eli'.encode()).hexdigest()
            session['data'] = mfp.get_all()
            return redirect(url_for('index'))
        else:
            return render_template("login.html", status=status)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
@app.route('/api')
def api():
    return jsonify(mfp.get_all())

@app.route('/load_ajax', methods=["POST"])
def load_ajax():
    session["data"] = request.json["data"]
    #print(session['data'])
    return redirect(url_for('home')) 


if __name__ == "__main__":
    app.run(debug=True)