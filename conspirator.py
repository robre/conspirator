
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import uuid
import json
import os
import jobs

app = Flask(__name__)

def get_targets():
    with open("target_db.json", "r") as tDB:
        return json.load(tDB)

def add_target(target,uid):
    tDB = get_targets()
    tDB[uid] = {'target': target}
    with open("target_db.json", "w") as tDBw:
        json.dump(tDB,tDBw)
    return True
    
def valid_target(target):
    if ";" in target or "|" in target or '"' in target or "'" in target or "$" in target or '`' in target:
        return False
    if "http" in target[:5]:
        return True
    else:
        return False

def initialize(target, uid):
    add_target(target, uid)
    os.mkdir("targets/{}".format(uid)) # Create Directory for this Target
    description = {"target": target, "uuid": uid}
    with open("targets/{}/about.json".format(uid), "w+") as site: # Create a json file
        json.dump(description,site)
    jobs.nmap_scan(target,uid)
    jobs.ffuf_scan(target,uid)
    
    # Enqueue Jobs
    # Create NMAP
    # CREATE FFUF
    # Enqueue Jobs using Redis

@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method=='POST':
        target = request.form['target']
        if valid_target(target):
            uid = str(uuid.uuid4())
            initialize(target, uid)
            return redirect(url_for("dashboard", uid=uid))
        else:
            return "Error - invalid Target"
    else:
        targets = get_targets()
        return render_template("index.html", targets=targets)

@app.route('/db/<uid>', methods=['GET'])
def dashboard(uid):
    t = get_targets()
    if uid in t:
        return render_template("dashboard.html", target={'target': t[uid], 'uid': uid})
    else:
        return "Error - invalid UUID"

@app.route('/targets/<uid>/<filename>')
def data(uid,filename):
    t = get_targets()
    if uid in t:
        return send_from_directory('targets/{}'.format(uid),filename)
    else:
        error = {'Error': '404'}
        return jsonify(error)




