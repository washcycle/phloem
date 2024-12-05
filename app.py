
import sqlite3
import uuid
import requests
import logging
import datetime
import os
from flask import Flask, render_template, g, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
import paramiko
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WireGuardCmdFactory:
    
    add_peer = "wg set wg0 peer {peer_public_key} allowed-ips {}/32"
    

class Peer(db.Model):
    __tablename__ = 'peers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    device = db.Column(db.String)
    ip_address = db.Column(db.String)
    public_key = db.Column(db.String)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime)     

def create_peer(peer):
    rsakey = secretClient.get_secret("pkey").value
    rsakey = rsakey.replace('- ', '-\n').replace(' -', '\n-')
    pkey = paramiko.RSAKey.from_private_key(StringIO(rsakey))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    client.connect('10.10.6.8', username='azureuser', pkey=pkey)
    stdin, stdout, stderr = client.exec_command('ls ~/')
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()

@app.route('/')
@app.route('/index')
def homepage():
    peers = Peer.query.all()    
    return render_template('index.html', peers=peers)

@app.route('/peer', methods=["GET", "POST"])
def peer():
    j = request.get_json()
    if j['action'] == "delete":
        continue
    elif j['action'] == "edit":
        continue
    resp = jsonify(success=True)
    return resp


@app.route('/add', methods=["GET", "POST"])
def add_peer():
    if request.method == "POST":

        peer = Peer(user_id = request.form.get('user_id'),
                    device = request.form.get('device'),
                    ip_address = request.form.get('ip_address'),
                    public_key = request.form.get('public_key'))        
        db.session.add(peer)
        create_peer(peer)
        db.session.commit()
        peers = Peer.query.all()
        return render_template('index.html', peers=peers)   
    else:
        resp = jsonify(success=True)
        return resp

if __name__ == '__main__':
    app.run()