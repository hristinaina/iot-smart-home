import random
import time


def generate_value():
    n = time.ctime()[11:13] + time.ctime()[14:16]
    return "{}:{}".format(n[0:2], n[2:])


def run_b4sd_simulator(delay, callback, stop_event, publish_event, settings):
    while True:
        time_value = generate_value()
        callback(time_value, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
