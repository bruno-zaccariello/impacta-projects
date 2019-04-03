import requests
from flask import Flask, request, jsonify, make_response, render_template
import json
import os

from flask import Flask
app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

grant_type = 'authorization_code'
redirect_uri = 'http://localhost:5000/callback'

TOKEN = str()

@app.route('/')
def hello_world():
    nome = 'teste'
    return render_template("index.html", nome=nome)

@app.route('/callback')
def receive_code():
    TOKEN = request.args.get('code')
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "redirect_uri": redirect_uri,
        "code": TOKEN
        }
    r = requests.post('https://api.instagram.com/oauth/access_token', data=payload)
    body = r.json()
    token = body['access_token']
    if token:
        SELF_URL = 'https://api.instagram.com/v1/users/self/'
        RECENT_URL = 'https://api.instagram.com/v1/users/self/media/recent'
        recentData = requests.get(RECENT_URL, params={'access_token':token}).json()
        selfData = requests.get(SELF_URL, params={'access_token':token}).json()
        print(recentData)
        print(selfData)
        return render_template('insta.html', post=recentData, prof=selfData)
    else:
        return render_template('insta.html', post=dict(), prof=dict())


@app.route('/insta')
def gram():    
    url = 'https://api.instagram.com/v1/users/self/media/recent'
    r = requests.get(url, params={'access_token':TOKEN})
    data = r.json()
    return render_template("insta.html", insta=data)


if __name__ == '__main__':
    app.run(debug=True)
