
import threading
import time

from simulators.uds import run_uds_simulator


def uds_callback(distance, name):
    t = time.localtime()
    print("=" * 10 + name + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Distance: {distance}cm")


def run_uds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        uds_thread = threading.Thread(target=run_uds_simulator, args=(2, uds_callback, stop_event, settings["name"]))
        uds_thread.start()
        threads.append(uds_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.uds import run_uds_loop, UDS
        print("Starting {} loop".format(settings["name"]))
        uds = UDS(settings["trig_pin"],settings["echo_pin"],settings["max_iter"],settings["name"])
        uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print("{} loop started".format(settings["name"]))
