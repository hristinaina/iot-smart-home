import multiprocessing
import threading

from components.b4sd import run_b4sd
from components.infrared import run_infrared
from components.rgb import run_rgb
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta
from time import sleep

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

bb_alarm_time = "21:39"
buzzer_stop_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    client.subscribe("front-bb")
    client.subscribe("front-bb-off")

def update_data(topic, data):
    print("bb data: ", data, "received from topic " + topic)
    if topic == "front-bb":
        global bb_alarm_time
        bb_alarm_time = data["time"]
    elif topic == "front-bb-off":
        buzzer_stop_event.set()

def connect_mqtt():
    # MQTT Configuration
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


def run_alarm_clock(bb_settings, threads, buzzer_stop_event):
    is_active = False
    time_difference = timedelta(seconds=7)
    while True:
        target_time = datetime.strptime(bb_alarm_time, "%H:%M").time()
        current_time = datetime.now().time()

        delta_target_time = datetime.combine(datetime.today(), target_time)
        delta_target_time = delta_target_time + time_difference
        max_target_time = delta_target_time.time()

        if target_time <= current_time <= max_target_time and not is_active:
            buzzer_stop_event.clear()
            run_buzzer(bb_settings, threads, buzzer_stop_event)
            is_active = True
        if buzzer_stop_event.is_set():
            is_active = False
        sleep(5)


def menu():
    print("="*10 + "  MENU  " + "="*10)
    print("-- Enter B to activate buzzer --")
    print("-- Enter D to deactivate buzzer --")
    print("-- Enter X to stop all devices --")
    print("=" * 30)


if __name__ == "__main__":
    print('Starting PI3')
    connect_mqtt()
    menu()
    settings = load_settings('settings3.json')
    threads = []

    stop_event = threading.Event()
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

        alarm_clock_thread = threading.Thread(target=run_alarm_clock, args=(bb_settings, threads, buzzer_stop_event))
        alarm_clock_thread.start()
        threads.append(alarm_clock_thread)

        while True:
            user_input = input().strip().upper()
            if user_input == "X":
                stop_event.set()
                buzzer_stop_event.set()
            if user_input == "B":
                buzzer_stop_event.clear()
                run_buzzer(bb_settings, threads, buzzer_stop_event)
            elif user_input == "D":
                buzzer_stop_event.set()

    except KeyboardInterrupt:
        print('\nStopping app')
        for t in threads:
            stop_event.set()
