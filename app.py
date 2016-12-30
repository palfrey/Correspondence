from flask import Flask, render_template, request
import logging
import requests
import os
import json

app = Flask(__name__)
server_url = os.environ["SERVER_URL"]
table = "mailing"
table_url = "%s/%s"%(server_url, table)

table_req = requests.get(table_url)
if table_req.status_code == 404:
    create = requests.post("%s/_config/%s" % (server_url, table), data=json.dumps({"op": "set", "change": {"crdt": "ORSET"}}))
    create.raise_for_status()

@app.route("/")
def index():
    return render_template("%s.html" % crdt, table=data[0], table_name=table, extra=extra)

if __name__ == "__main__":
    app.run()