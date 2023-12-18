import RPi.GPIO as GPIO
import time


class Buzzer:

    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        GPIO.setup(pin, GPIO.OUT)


def run_buzzer_sensor(buzzer, callback_activated, callback_deactivated, delay, stop_event, publish_event, settings):
    callback_activated(publish_event, settings)
    while True:
        GPIO.output(buzzer.pin, True)
        time.sleep(delay)
        GPIO.output(buzzer.pin, False)
        if stop_event.is_set():
            callback_deactivated(publish_event, settings)
            break
        time.sleep(delay)
