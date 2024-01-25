import json
import threading

from paho.mqtt import publish

from simulators.buzzer import run_buzzer_simulator
import time
from settings import lock, HOSTNAME, PORT

buzzer_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, buzzer_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = buzzer_batch.copy()
            publish_data_counter = 0
            buzzer_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} buzzer values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzzer_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def buzzer_activated(publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Buzzer activated")

    payload = {
        "measurement": "Buzzer_active",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": "activated",
        "is_last": False
    }

    with counter_lock:
        if publish_data_counter + 1 >= publish_data_limit:
            payload["is_last"] = True
        buzzer_batch.append(('data/buzzer', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def buzzer_deactivated(publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Buzzer deactivated")

    payload = {
        "measurement": "Buzzer_active",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": "deactivated",
        "is_last": False
    }

    with counter_lock:
        if publish_data_counter + 1 >= publish_data_limit:
            payload["is_last"] = True
        buzzer_batch.append(('data/buzzer', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_buzzer(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(2, buzzer_activated, buzzer_deactivated,
                                                                            stop_event, publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.buzzer import run_buzzer_sensor, Buzzer
        print("Starting {} loop".format(settings["name"]))
        buzzer = Buzzer(settings["pin"], settings['name'])
        buzzer_thread = threading.Thread(target=run_buzzer_sensor, args=(buzzer, buzzer_activated, buzzer_deactivated,
                                                                         2, stop_event, publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("{} loop started".format(settings["name"]))