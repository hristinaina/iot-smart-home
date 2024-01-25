#!/usr/bin/env python3
import json

import paho.mqtt.client as mqtt

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime


humidity = 0
temperature = 0
DHT_NAME = "GDHT"


def on_connect(client, userdata, flags, rc):
    client.subscribe("data/temperature")
    client.subscribe("data/humidity")


def update_data(topic, data):
    global humidity, temperature
    if data["name"] == DHT_NAME:
        if topic == "data/temperature":
            temperature = data["value"]
        elif topic == "data/humidity":
            humidity = data["value"]


def connect_mqtt():
    # MQTT Configuration
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


def create_lcd_and_adapter(settings):
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print('I2C Address Error !')
            exit(1)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=settings["pin_rs"], pin_e=settings["pin_e"], pins_db=settings["pins_db"], GPIO=mcp)
    return lcd, mcp


def run_lcd_loop(lcd, mcp, delay, callback, stop_event, settings):
    mcp.output(3, 1)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns
    connect_mqtt()
    while True:
        lcd.clear()
        lcd.setCursor(0, 0)  # set cursor position
        lcd.message("Humidity: ", humidity)
        lcd.message("Temperature: ", temperature)
        callback(humidity, temperature, settings)
        if stop_event.is_set():
            break
        sleep(delay)



