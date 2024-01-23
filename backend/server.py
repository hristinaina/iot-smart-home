import time

from flask_socketio import SocketIO
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import settings

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", async_mode='threading')

# InfluxDB Configuration
token = "test_token"
org = "test_org"
url = "http://localhost:8086"
bucket = "test_bucket"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# Table names: Temperature, Humidity, PIR_motion, Button_pressed, Buzzer_active, Light_status, MS_password, UDS,
#              Acceleration, Gyroscope, Infrared
# Topic names: data/temperature, data/humidity, data/pir, data/button, data/buzzer, data/light, data/ms, data/uds,
#              data/acceleration, data/gyroscope, data/ir


def on_connect(client, userdata, flags, rc):
    client.subscribe("data/+")

@socketio.on('connect')
def handle_connect():
    print('Client connected successfully\n')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected successfully\n')

def send_data_to_client(data):
    try:
        socketio.emit('data/'+data["runs_on"], {'message': data})
        print("Data sent to topic: data/" + data["runs_on"])
    except Exception as e:
        print(e)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))


def save_to_db(topic, data):
    print("Saving data to database: ", data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if topic == "data/acceleration" or topic == "data/gyroscope":
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .tag("axis", data["axis"])
            .field(data["field_name"], data["value"])
        )
    else:
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field(data["field_name"], data["value"])
        )
    write_api.write(bucket=bucket, org=org, record=point)
    send_data_to_client(data)


@app.route('/api/devices/<pi_id>', methods=['GET'])
@cross_origin()
def get_devices(pi_id):
    id = pi_id[-1]
    data = settings.load_settings("../settings" + id + ".json")
    device_list = list(data.values())
    return device_list


if __name__ == '__main__':
    app.run(debug=True,  port=8000)
