import json
import threading
import time

from paho.mqtt import publish

from settings import lock, HOSTNAME, PORT
from simulators.b4sd import run_b4sd_simulator
from simulators.ms import run_ms_simulator


def b4sd_callback(time_value, b4sd_settings):
    t = time.localtime()
    print("=" * 10 + b4sd_settings["name"] + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Time: {time_value}")


def run_b4sd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(2, b4sd_callback, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.b4sd import run_b4sd_loop, B4SD
        print("Starting {} loop".format(settings["name"]))
        b4sd = B4SD(settings)
        b4sd_thread = threading.Thread(target=run_b4sd_loop, args=(b4sd, 2, b4sd_callback, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("{} loop started".format(settings["name"]))
