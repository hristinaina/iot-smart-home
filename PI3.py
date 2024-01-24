import json
import multiprocessing
import threading

import paho.mqtt.client as mqtt

from components.b4sd import run_b4sd
from components.button import run_button
from components.infrared import run_infrared
from components.lcd import run_lcd
from components.ms import run_ms
from components.button import run_button
from components.light import run_light
from components.ms import run_ms
from components.rgb import run_rgb
from components.uds import run_uds
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("pi3")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: user_inputs(json.loads(msg.payload.decode('utf-8')))


def user_inputs(data):
    while True:
        if data["trigger"] == "B":
            buzzer_stop_event.clear()
            run_buzzer(bb_settings, threads, buzzer_stop_event)
        elif data["trigger"] == "D":
            buzzer_stop_event.set()
        elif data["trigger"] == "X":
            stop_event.set()
            buzzer_stop_event.set()


def menu():
    print("="*10 + "  MENU  " + "="*10)
    print("-- Enter B to activate buzzer --")
    print("-- Enter D to deactivate buzzer --")
    print("-- Enter X to stop all devices --")
    print("=" * 30)


if __name__ == "__main__":
    print('Starting PI3')
    menu()
    settings = load_settings('settings3.json')
    threads = []

    stop_event = threading.Event()
    buzzer_stop_event = threading.Event()
    try:
        rdht4_settings = settings['RDHT4']
        rpir4_settings = settings['RPIR4']
        bb_settings = settings['BB']
        bir_settings = settings['BIR']
        brgb_settings = settings['BRGB']
        b4sd_settings = settings['B4SD']

        run_dht(rdht4_settings, threads, stop_event)
        run_pir(rpir4_settings, threads, stop_event)
        run_infrared(bir_settings, threads, stop_event)
        run_rgb(brgb_settings, threads, stop_event)
        run_b4sd(b4sd_settings, threads, stop_event)



    except KeyboardInterrupt:
        print('\nStopping app')
        for t in threads:
            stop_event.set()
