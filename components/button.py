import json
import threading

from paho.mqtt import publish

from simulators.button import run_button_simulator
import time
from settings import lock, HOSTNAME, PORT

button_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()


def publisher_task(event, button_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = button_batch.copy()
            publish_data_counter = 0
            button_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} button values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, button_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def button_pressed(publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("The door are OPENED")

    payload = {
        "measurement": "Button_pressed",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": "pressed"
    }

    with counter_lock:
        button_batch.append(('data/button', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def button_released(publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("The door are CLOSED")

    payload = {
        "measurement": "Button_pressed",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": "released"
    }

    with counter_lock:
        button_batch.append(('data/button', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_pressed, button_released, stop_event, publish_event, settings))
        button_thread.start()
        threads.append(button_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.button import run_button_loop, Button
        print("Starting {} loop".format(settings["name"]))
        button = Button(settings["pin"], settings['name'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, button_pressed, button_released, stop_event, publish_event, settings))
        button_thread.start()
        threads.append(button_thread)
        print("{} loop started".format(settings["name"]))