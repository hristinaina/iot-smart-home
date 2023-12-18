import json
import threading

from paho.mqtt import publish

from simulators.pir import run_pir_simulator
import time
from settings import lock, HOSTNAME, PORT

pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def motion_callback(publish_event, dht_settings, value, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Detected motion")

    payload = {
        "measurement": "PIR_motion",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": value
    }

    with counter_lock:
        pir_batch.append(('data/pir', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, motion_callback, stop_event, publish_event, settings))
        pir_thread.start()
        threads.append(pir_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.pir import run_pir_loop, PIR
        print("Starting {} loop".format(settings["name"]))
        pir = PIR(settings["pin"], settings['name'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, motion_callback, stop_event, publish_event, settings))
        pir_thread.start()
        threads.append(pir_thread)
        print("{} loop started".format(settings["name"]))