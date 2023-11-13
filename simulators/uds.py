import random
import time


def generate_values(initial_distance=10):
    distance = initial_distance
    sing = 1
    while True:
        distance = distance + random.randint(1, 5)*sing
        if distance>100 or distance< 5:
            sing*=-1
        yield distance


def run_uds_simulator(delay, callback, stop_event, name):
    for distance in generate_values():
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(distance,name)
        if stop_event.is_set():
            break