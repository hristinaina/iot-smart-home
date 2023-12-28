import json
import threading

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
import time

from simulators.light import run_light_simulator

light_batch = []
publish_data_counter = 0
publish_data_limit = 3
counter_lock = threading.Lock()


def publisher_task(event, light_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = light_batch.copy()
            publish_data_counter = 0
            light_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} light values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, light_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def light_callback(state, publish_event, dht_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Light on: {state}")

    payload = {
        "measurement": "Light_state",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": "on" if state else "off"
    }

    with counter_lock:
        light_batch.append(('data/light', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_light(pipe, settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        uds_thread = threading.Thread(target=run_light_simulator,
                                      args=(pipe, 2, light_callback, stop_event, publish_event, settings))
        uds_thread.start()
        threads.append(uds_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.light import run_light_loop, light
        print("Starting {} loop".format(settings["name"]))
        l = light(settings["name"], settings["pin"])
        uds_thread = threading.Thread(target=run_light_loop,
                                      args=(pipe, l, 2, light_callback, stop_event, publish_event, settings))
        uds_thread.start()
        threads.append(uds_thread)
        print("{} loop started".format(settings["name"]))
