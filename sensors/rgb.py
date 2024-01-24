import json

import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt


new_action = "off"

def map_key_to_color(key):
    match key:
        case "1":
            return "red"
        case "2":
            return "green"
        case "3":
            return "blue"
        case "4":
            return "yellow"
        case "5":
            return "lightBlue"
        case "6":
            return "purple"
        case "0":
            return "off"
        case _:
            return "white"  # Default color for unknown keys

def on_connect(client, userdata, flags, rc):
    client.subscribe("data/ir")
    client.subscribe("front-rgb")

def update_data(topic, data):
    global new_action
    print("rgb data: ", data, "received from topic " + topic)
    new_action = map_key_to_color(data["value"])

def connect_mqtt():
    # MQTT Configuration
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


class RGB:
    def __init__(self, settings):
        self.red_pin = settings['red_pin']
        self.blue_pin = settings['blue_pin']
        self.green_pin = settings['green_pin']
        self.status = "off"
        self.name = settings['name']
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)

    def turnOff(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def white(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def red(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def green(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def yellow(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def purple(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def lightBlue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)


def change_light(rgb):
    if rgb.status == "red":
        rgb.red()
    elif rgb.status == "blue":
        rgb.blue()
    elif rgb.status == "green":
        rgb.green()
    elif rgb.status == "yellow":
        rgb.yellow()
    elif rgb.status == "purple":
        rgb.purple()
    elif rgb.status == "lightBlue":
        rgb.lightBlue()
    elif rgb.status == "white":
        rgb.white()
    elif rgb.status == "off":
        rgb.turnOff()


def run_rgb_loop(rgb, delay, callback, stop_event, publish_event, settings):
    rgb.turnOff()
    while True:
        if new_action != rgb.status:
            rgb.status = new_action
            change_light(rgb)
            callback(rgb.status, publish_event, settings)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        sleep(delay)

