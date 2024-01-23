from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# InfluxDB Configuration
token = "test_token"
org = "test_org"
url = "http://localhost:8086"
bucket = "test_bucket"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 0)
mqtt_client.loop_start()
in_house = 0


# Table names: Temperature, Humidity, PIR_motion, Button_pressed, Buzzer_active, Light_status, MS_password, UDS,
#              Acceleration, Gyroscope
# Topic names: data/temperature, data/humidity, data/pir, data/button, data/buzzer, data/light, data/ms, data/uds,
#              data/acceleration, data/gyroscope


def on_connect(client, userdata, flags, rc):
    client.subscribe("data/+")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))


def adjust_people_count(device_number=1):
    with app.app_context():
        query = ('from(bucket: "test_bucket") |> range(start: -5s, stop: now()) |> filter(fn: ('
                 'r) => r["_measurement"] == "UDS") |> filter(fn: (r) => r["name"] == "DUS' + str(
            device_number) + '")  |> yield(name: "last")')
        response = handle_influx_query(query)
        values = json.loads(response.data.decode('utf-8'))['data']
        values_list = [item["_value"] for item in values]
        gain = sum([j - i for i, j in zip(values_list[:-1], values_list[1:])])

        global in_house
        if len(values) > 0:
            if gain > 0:
                in_house += 1
            elif gain < 0:
                in_house -= 1
            if in_house < 0:
                in_house = 0

        point = (
            Point("People_count")
            .tag("name", "overall")
            .field("population", in_house)
        )
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)


def command_callback(data):
    # if data["measurement"] == "Buzzer_active":
    #     if data["value"] == "on":
    #         mqtt_client.publish("pi1", json.dumps({"trigger": "B"}))
    #     elif data["value"] == "off":
    #         mqtt_client.publish("pi1", json.dumps({"trigger": "D"}))
    # elif data["measurement"] == "Light_status":
    #     if data["value"] == "on":
    #         mqtt_client.publish("pi1", json.dumps({"trigger": "L"}))
    #     elif data["value"] == "off":
    #         mqtt_client.publish("pi1", json.dumps({"trigger": "X"}))

    if data["name"] == "DPIR1" and data['value'] == "detected":
        mqtt_client.publish("pi1", json.dumps({"trigger": "L"}))
        adjust_people_count()
    if data["name"] == "DPIR2" and data['value'] == "detected":
        adjust_people_count(2)


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
    command_callback(data)


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
