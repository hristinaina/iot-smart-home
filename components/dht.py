import json

from paho.mqtt import publish

from simulators.dht import run_dht_simulator
import threading
import time
from settings import lock, HOSTNAME, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + dht_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": temperature,
        "is_last": False
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "field_name": dht_settings["field_name"],
        "value": humidity,
        "is_last": False
    }

    with counter_lock:
        if publish_data_counter + 1 >= publish_data_limit:
            humidity_payload["is_last"] = True
            temp_payload["is_last"] = True
        dht_batch.append(('data/temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('data/humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting {} loop".format(settings["name"]))
        dht = DHT(settings["name"], settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("{} loop started".format(settings["name"]))
