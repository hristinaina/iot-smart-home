import random
import time


def generate_value():
    if random.randint(1, 2) == 2:
        return True
    return False


def run_pir_simulator(delay, callback, stop_event, publish_event, settings):
    while True:
        motion_detected = generate_value()
        time.sleep(delay)  # Delay between readings (adjust as needed)
        if motion_detected:
            callback(publish_event, settings)
        if stop_event.is_set():
            break
