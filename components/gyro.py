import json

from paho.mqtt import publish

from simulators.dht import run_dht_simulator
import threading
import time
from settings import lock, HOSTNAME, PORT
from simulators.gyro import run_gyro_simulator

gyro_batch = []
publish_data_counter = 0
publish_data_limit = 6
counter_lock = threading.Lock()


def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gyro_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        publish.multiple(local_gyro_batch, hostname=HOSTNAME, port=PORT)
        print(f'Published {publish_data_limit} gyro values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gyro_callback(accel, gyro, publish_event, gyro_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 10 + gyro_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Acceleration: {accel}%")
        print(f"Gyroscope: {gyro}°C")

    accel_payloads = []
    gyro_payloads = []
    axis = ["x", "y", "z"]
    for i in range(3):
        accel_payload = {
            "measurement": "Acceleration",
            "simulated": gyro_settings['simulated'],
            "runs_on": gyro_settings["runs_on"],
            "name": gyro_settings["name"],
            "field_name": gyro_settings["field_name"],
            "axis": axis[i],
            "value": accel[i]
        }
        gyro_payload = {
            "measurement": "Gyroscope",
            "simulated": gyro_settings['simulated'],
            "runs_on": gyro_settings["runs_on"],
            "name": gyro_settings["name"],
            "field_name": gyro_settings["field_name"],
            "axis": axis[i],
            "value": gyro[i]
        }
        accel_payloads.append(accel_payload)
        gyro_payloads.append(gyro_payload)

    with counter_lock:
        for payload in accel_payloads:
            gyro_batch.append(('data/acceleration', json.dumps(payload), 0, True))
        for payload in gyro_payloads:
            gyro_batch.append(('data/gyroscope', json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        gyro_thread = threading.Thread(target=run_gyro_simulator, args=(2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.Gyro.gyro import run_gyro_loop, MPU6050
        print("Starting {} loop".format(settings["name"]))
        mpu = MPU6050.MPU6050()
        gyro_thread = threading.Thread(target=run_gyro_loop, args=(mpu, 2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print("{} loop started".format(settings["name"]))
