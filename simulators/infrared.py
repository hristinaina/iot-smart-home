import time
import random

buttons_names = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0", "#"]
# String list in same order as HEX list

def get_key():
        index = random.randint(0, len(buttons_names) - 1)
        return buttons_names[index]


def run_ir_simulator(delay, callback, stop_event, publish_event, settings):
    while True:
        key = get_key()
        callback(key, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
