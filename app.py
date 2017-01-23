from flask import Flask, render_template, request, redirect
import logging
import requests
import os
import json
import uuid

app = Flask(__name__)
app.debug = True
server_url = os.environ["SERVER_URL"]
table = "mailing"
table_url = "%s/%s"%(server_url, table)

table_req = requests.get(table_url)
if table_req.status_code == 404:
    create = requests.post("%s/_config/%s" % (server_url, table),
        data=json.dumps({"op": "set", "change": {"crdt": "ORSET"}}))
    create.raise_for_status()

@app.route("/new", methods = ['POST'])
def create():
    print("form", request.form)
    name = request.form["name"]
    create = requests.post("%s/%s" % (table_url, name),
        data=json.dumps({"op": "create", "change": {}}))
    create.raise_for_status()
    return redirect("/list/%s" % name)

@app.route("/list/<list_name>")
def list_display(list_name):
    list_url = "%s/%s" % (table_url, list_name)
    list_entries = requests.get(list_url)
    list_entries.raise_for_status()
    list_entries = list_entries.json()
    subscribers = set([x["item"] for x in list_entries if x["metadata"]["acknowledged"]])
    pending = set([x["item"] for x in list_entries if not x["metadata"]["acknowledged"]])
    return render_template("showlist.html", list_name=list_name, subscribers=subscribers, pending=pending)

@app.route("/list/<list_name>", methods = ['POST'])
def list_add(list_name):
    list_url = "%s/%s" % (table_url, list_name)
    data = {
        "op": "add",
        "change": {
            "key": str(uuid.uuid4()),
            "item": request.form["subscriber"],
            "metadata": {"acknowledged": False}
        }
    }
    add = requests.post(list_url, data=json.dumps(data))
    add.raise_for_status()
    return redirect("/list/%s" % list_name)

@app.route("/")
def index():
    mailings = requests.get(table_url).json()
    return render_template("index.html", mailings=sorted(mailings))

if __name__ == "__main__":
    app.run()