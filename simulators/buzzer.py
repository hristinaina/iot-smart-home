import winsound
import time


def play_sound(delay):
    frequency = 1000
    winsound.Beep(frequency, delay * 1000)


def run_buzzer_simulator(delay, callback_activated, callback_deactivated, name, stop_event):
    callback_activated(name)
    while True:
        play_sound(delay)
        if stop_event.is_set():
            callback_deactivated(name)
            break
        time.sleep(delay)
