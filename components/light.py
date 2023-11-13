import threading

from settings import lock
import time

from simulators.light import run_light_simulator


def light_callback(state, name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Light on: {state}")


def run_light(pipe, settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        uds_thread = threading.Thread(target=run_light_simulator,
                                      args=(pipe, 2, light_callback, stop_event, settings["name"]))
        uds_thread.start()
        threads.append(uds_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.light import run_light_loop, light
        print("Starting {} loop".format(settings["name"]))
        l = light(settings["pin"], settings["name"])
        uds_thread = threading.Thread(target=run_light_loop, args=(l, 2, light_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print("{} loop started".format(settings["name"]))
