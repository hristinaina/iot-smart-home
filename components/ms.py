import json
import threading
import time

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
from simulators.ms import run_ms_simulator


ms_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, ms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = ms_batch.copy()
            publish_data_counter = 0
            ms_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} ms values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ms_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ms_callback(code, publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
    payload = {
        "measurement": "MS_password",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": code,
        "is_last": False
    }

    with counter_lock:
        if publish_data_counter + 1 >= publish_data_limit:
            payload["is_last"] = True
        ms_batch.append(('data/ms', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        ms_thread = threading.Thread(target=run_ms_simulator, args=(2, ms_callback, stop_event, publish_event, settings))
        ms_thread.start()
        threads.append(ms_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.ms import run_ms_loop, MS
        print("Starting {} loop".format(settings["name"]))
        ms = MS(settings)
        ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event, publish_event, settings))
        ms_thread.start()
        threads.append(ms_thread)
        print("{} loop started".format(settings["name"]))
