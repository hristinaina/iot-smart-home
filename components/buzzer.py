import threading
from simulators.buzzer import run_buzzer_simulator
import time
from settings import lock


def buzzer_activated(name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Buzzer activated")


def buzzer_deactivated(name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Buzzer deactivated")


def run_buzzer(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(2, buzzer_activated, buzzer_deactivated,
                                                                            settings["name"], stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.buzzer import run_buzzer_sensor, Buzzer
        print("Starting {} loop".format(settings["name"]))
        buzzer = Buzzer(settings["pin"], settings['name'])
        buzzer_thread = threading.Thread(target=run_buzzer_sensor, args=(buzzer, buzzer_activated, buzzer_deactivated,
                                                                         2, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("{} loop started".format(settings["name"]))