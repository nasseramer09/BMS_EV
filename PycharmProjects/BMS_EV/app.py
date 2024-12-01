import time
from http.client import responses
from threading import Thread
from urllib import request
from flask_socketio import SocketIO

import requests
from flask import Flask, render_template

app = Flask(__name__)
socketio = SocketIO(app)
url = "http://127.0.0.1:5000/"


def connection_handler():
    while True:
        time.sleep(1)
        response = requests.get(f"{url}/info")
        if response.status_code == 200:
            data = response.json()
            socketio.emit('update_time',
                          {'sim_time_hour':data['sim_time_hour'],
                                 'sim_time_min':data['sim_time_min']
                                      })
@app.route('/')
def home_page():  # put application's code here

    responses = requests.get(url)
    data = responses.json()
    return render_template("home.html", data=data)

@app.route('/info')
def info():
    responses = requests.get(f"{url}/info")
    data = responses.json()
    return render_template("info.html", data=data )

@app.route('/priceperhour')
def priceperhour():
    responses = requests.get(f"{url}/priceperhour")
    data = responses.json()
    return render_template("priceperhour.html", data=data)


if __name__ == '__main__':
    thread = Thread(target=connection_handler)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
