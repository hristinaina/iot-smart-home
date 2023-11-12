import threading
import time
from settings import lock
from simulators.ms import run_ms_simulator


def ms_callback(code, name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")


def run_ms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        ms_thread = threading.Thread(target=run_ms_simulator, args=(2, ms_callback, stop_event, settings["name"]))
        ms_thread.start()
        threads.append(ms_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.ms import run_ms_loop, MS
        print("Starting {} loop".format(settings["name"]))
        ms = MS(settings)
        ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
        print("{} loop started".format(settings["name"]))
