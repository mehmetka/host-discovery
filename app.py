import os
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    con = sqlite3.connect("/opt/discovery.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT uid, ip, mac, os, datetime(created, 'unixepoch') FROM hosts")
   
    hostResults = cur.fetchall()
    return render_template('hosts.html', hosts = hostResults)

@app.route("/hosts/<hostID>/ports")
def openPorts(hostID):
    con = sqlite3.connect("/opt/discovery.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    paramHostID = (hostID,)
    cur.execute("SELECT h.ip, op.port FROM hosts h INNER JOIN open_ports op ON h.ip = op.ip WHERE h.uid = ?", paramHostID)
   
    openPortsResults = cur.fetchall()
    return render_template('open-ports.html', ports = openPortsResults)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
