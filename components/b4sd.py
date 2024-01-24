import json
import threading
import time

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
from simulators.b4sd import run_b4sd_simulator
from simulators.ms import run_ms_simulator


b4sd_batch = []
publish_data_counter = 0
publish_data_limit = 4
counter_lock = threading.Lock()


def publisher_task(event, b4sd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = b4sd_batch.copy()
            publish_data_counter = 0
            b4sd_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'Showed {publish_data_limit} b4sd values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, b4sd_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def b4sd_callback(time_value, publish_event, b4sd_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + b4sd_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Time: {time_value}")

    payload = {
        "measurement": "Time_b4sd",
        "simulated": b4sd_settings['simulated'],
        "runs_on": b4sd_settings["runs_on"],
        "name": b4sd_settings["name"],
        "field_name": b4sd_settings["field_name"],
        "value": time_value,
        "is_last": False
    }

    with counter_lock:
        if publish_data_counter + 1 >= publish_data_limit:
            payload["is_last"] = True
        b4sd_batch.append(('data/b4sd', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_b4sd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(2, b4sd_callback, stop_event, publish_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.b4sd import run_b4sd_loop, B4SD
        print("Starting {} loop".format(settings["name"]))
        b4sd = B4SD(settings)
        b4sd_thread = threading.Thread(target=run_b4sd_loop, args=(b4sd, 2, b4sd_callback, stop_event, publish_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("{} loop started".format(settings["name"]))
