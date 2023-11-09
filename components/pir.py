import threading
from simulators.pir import run_pir_simulator
import time
from settings import lock


def motion_detected(name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("{0} detected motion".format(name))


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, motion_detected, stop_event, settings["name"]))
        pir_thread.start()
        threads.append(pir_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.pir import run_pir_loop, PIR
        print("Starting {} loop".format(settings["name"]))
        pir = PIR(settings["pin"], settings['name'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, motion_detected, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print("{} loop started".format(settings["name"]))