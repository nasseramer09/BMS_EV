import time
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
                                 'sim_time_min':data['sim_time_min'],
                                    'base_current_load':data['base_current_load'],
                                    'battery_capacity_kWh':data['battery_capacity_kWh'],
                                      })
@app.route('/')
def home_page():  # put application's code here

    responses = requests.get(url)
    if responses.status_code == 200:
        data = responses.json()
        return render_template("home.html", data=data)

@app.route('/info')
def info():

    responses = requests.get(f"{url}/info")
    if responses.status_code == 200:
        data = responses.json()
        return render_template("info.html", data=data )

@app.route('/priceperhour')
def priceperhour():
    responses = requests.get(f"{url}/priceperhour")
    if responses.status_code==200:
        data = responses.json()
        return render_template("priceperhour.html", data=data)

@app.route('/baseload')
def baseload():
    responses = requests.get(f"{url}/baseload")
    if responses.status_code==200:
        data = responses.json()
        return render_template("baseload.html", data=data)

@app.route('/batteryStatus', methods=['GET'])
def batteryStatus():
    responses = requests.get(f"{url}/info")
    if responses.status_code == 200:
        data = responses.json()
        return render_template("evBatteryStatus.html", data=data)

@app.route('/charging_handle', methods=['POST'])
def charging_handle():
    isCharging = request.json.get('charging')
    responses = requests.post(f"{url}/charge", json={"charging": isCharging})
    if responses.status_code == 200:
        return responses.json(), 200
    return 'fail to toggle charging', 500


if __name__ == '__main__':
    thread = Thread(target=connection_handler)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
