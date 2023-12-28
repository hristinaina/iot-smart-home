import json
import threading
import time

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
from simulators.uds import run_uds_simulator

uds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, uds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = uds_batch.copy()
            publish_data_counter = 0
            uds_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} uds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def uds_callback(distance, publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Distance: {distance}cm")

    payload = {
        "measurement": "UDS",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": distance
    }

    with counter_lock:
        uds_batch.append(('data/uds', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_uds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        uds_thread = threading.Thread(target=run_uds_simulator,
                                      args=(2, uds_callback, stop_event, publish_event, settings))
        uds_thread.start()
        threads.append(uds_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.uds import run_uds_loop, UDS
        print("Starting {} loop".format(settings["name"]))
        uds = UDS(settings["trig_pin"], settings["echo_pin"], settings["max_iter"], settings["name"])
        uds_thread = threading.Thread(target=run_uds_loop,
                                      args=(uds, 2, uds_callback, stop_event, publish_event, settings))
        uds_thread.start()
        threads.append(uds_thread)
        print("{} loop started".format(settings["name"]))
