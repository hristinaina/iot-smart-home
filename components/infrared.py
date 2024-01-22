import json
import threading
import time

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
from simulators.infrared import run_ir_simulator

ir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ir_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        publish.multiple(local_ir_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} infrared values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ir_callback(key, publish_event, ir_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + ir_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Key pressed: {key}")

    payload = {
        "measurement": "Infrared",
        "simulated": ir_settings['simulated'],
        "runs_on": ir_settings["runs_on"],
        "name": ir_settings["name"],
        "field_name": ir_settings["field_name"],
        "value": key
    }

    with counter_lock:
        ir_batch.append(('data/ir', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_infrared(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        ir_thread = threading.Thread(target=run_ir_simulator,
                                      args=(2, ir_callback, stop_event, publish_event, settings))
        ir_thread.start()
        threads.append(ir_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.infrared import run_ir_loop, Infrared
        print("Starting {} loop".format(settings["name"]))
        ir = Infrared(settings["pin"], settings["name"])
        ir_thread = threading.Thread(target=run_ir_loop,
                                      args=(ir, 2, ir_callback, stop_event, publish_event, settings))
        ir_thread.start()
        threads.append(ir_thread)
        print("{} loop started".format(settings["name"]))
