import random
import time


def generate_value(delay, previous_value=False):
    while True:
        time.sleep(delay)
        new_value = random.randint(1, 2) == 2
        if new_value == previous_value:
            continue
        else:
            previous_value = new_value
            yield new_value


def run_button_simulator(delay, callback_pressed, callback_released, stop_event, name):
    for pressed in generate_value(delay):
        if pressed:
            callback_pressed(name)
        else:
            callback_released(name)
        if stop_event.is_set():
            break
