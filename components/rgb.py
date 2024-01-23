import json

from paho.mqtt import publish

from simulators.dht import run_dht_simulator
import threading
import time
from settings import lock, HOSTNAME, PORT
from simulators.rgb import run_rgb_simulator

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} rgb values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(status, publish_event, rgb_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + rgb_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Status changed: {status}%")

    payload = {
        "measurement": "RGB",
        "simulated": rgb_settings['simulated'],
        "runs_on": rgb_settings["runs_on"],
        "name": rgb_settings["name"],
        "field_name": rgb_settings["field_name"],
        "value": status
    }

    with counter_lock:
        rgb_batch.append(('data/rgb', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rgb(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        rgb_thread = threading.Thread(target=run_rgb_simulator, args=(2, rgb_callback, stop_event, publish_event, settings))
        rgb_thread.start()
        threads.append(rgb_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.rgb import run_rgb_loop, RGB
        print("Starting {} loop".format(settings["name"]))
        rgb = RGB(settings)
        rgb_thread = threading.Thread(target=run_rgb_loop, args=(rgb, 2, rgb_callback, stop_event, publish_event, settings))
        rgb_thread.start()
        threads.append(rgb_thread)
        print("{} loop started".format(settings["name"]))
