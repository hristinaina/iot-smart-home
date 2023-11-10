from simulators.dht import run_dht_simulator
import threading
import time
from settings import lock


def dht_callback(humidity, temperature, code, name):
    with lock:
        t = time.localtime()
        print("=" * 10 + name + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event,settings["name"]))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.dht import run_dht_loop, DHT
        print("Starting {} loop".format(settings["name"]))
        dht = DHT(settings["name"], settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("{} loop started".format(settings["name"]))
