import json
import multiprocessing
import threading

import paho.mqtt.client as mqtt

from components.button import run_button
from components.ms import run_ms
from components.button import run_button
from components.light import run_light
from components.ms import run_ms
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

pi_light_pipe, light_pipe = multiprocessing.Pipe()

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("pi1")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: user_inputs(json.loads(msg.payload.decode('utf-8')))


def menu():
    print("=" * 10 + "  MENU  " + "=" * 10)
    print("-- Enter B to activate buzzer --")
    print("-- Enter D to deactivate buzzer --")
    print("-- Enter L to change light state --")
    print("-- Enter X to stop all devices --")
    print("=" * 30)


def user_inputs(data):
    while True:
        if data["trigger"] == "B":
            buzzer_stop_event.clear()
            run_buzzer(db_settings, threads, buzzer_stop_event)
        elif data["trigger"] == "D":
            buzzer_stop_event.set()
        elif data["trigger"] == "X":
            stop_event.set()
            buzzer_stop_event.set()
        elif data["trigger"] == "L":
            pi_light_pipe.send("l")


if __name__ == "__main__":
    print('Starting PI1')
    menu()
    settings = load_settings()
    threads = []

    stop_event = threading.Event()
    buzzer_stop_event = threading.Event()
    try:
        dht1_settings = settings['DHT1']
        dht2_settings = settings['DHT2']
        uds1_settings = settings['DUS1']
        rpir1_settings = settings['RPIR1']
        rpir2_settings = settings['RPIR2']
        dpir1_settings = settings['DPIR1']
        ds1_settings = settings['DS1']
        ms_settings = settings['DMS']
        db_settings = settings['DB']

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)
        run_uds(uds1_settings, threads, stop_event)
        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)
        run_button(ds1_settings, threads, stop_event)
        run_ms(ms_settings, threads, stop_event)

        run_light(light_pipe, settings['DL'], threads, stop_event)


    except KeyboardInterrupt:
        print('\nStopping app')
        for t in threads:
            stop_event.set()
