from flask import Flask, render_template, request, redirect, url_for,jsonify, session 
import importlib
from time import sleep
from hashlib import md5
from datetime import date
mfp = importlib.import_module("scrape_mfp")
compute = importlib.import_module("compute_mfp")
app = Flask(__name__)
app.config.from_object('config.DevConfig')
session = {}

@app.route('/', methods= ["GET"])
def index():
    if 'username' in session and 'data' not in session:
        username = session['username']
        return render_template('index.html', username=username) # user logged in but no data is found
                                                                # I should force a refresh here about every second 

    if 'username' in session and 'data' in session:             # both data and username are found 
        username = session['username']                          # display the data
        totals = session['data']['totals']
        measurements = session['data']['measurements']
        #computed = compute.compute(measurements["Weight"][0])
        #delta = compute.get_diff(totals,computed)
        #print(computed,delta)
        return render_template('index.html', username=username,
        totals=totals,
        measurements=measurements,
        )
    else:
        return redirect(url_for('login'))                       # if not logged in, redirect to login page
        
@app.route('/login', methods = ["GET", "POST"])
def login():
    
    if request.method == "GET":
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template("login.html")
    else:
        result = request.form.get("master_password")
        status = mfp.login(result)
        if status == "":
            session['username'] = md5('eli'.encode()).hexdigest()
            session["data"] = mfp.get_all()
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
    totals = {'totals':request.json["totals"]}
    exercise = {'exercise': request.json['exercise']}
    totals['totals'].update(exercise)
    measurements = {'measurements':request.json['measurements']}

    session["data"] = {**totals, **measurements} 
    return redirect(url_for('login')) 

if __name__ == "__main__":
    app.run(debug=True)
