import threading
from simulators.button import run_button_simulator
import time
from settings import lock


def button_pressed(name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("The door OPENED")


def button_released(name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("The door CLOSED")


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_pressed, button_released, stop_event, settings["name"]))
        button_thread.start()
        threads.append(button_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.button import run_button_loop, Button
        print("Starting {} loop".format(settings["name"]))
        button = Button(settings["pin"], settings['name'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, button_pressed, button_released, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print("{} loop started".format(settings["name"]))