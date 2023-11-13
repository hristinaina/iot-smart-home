import RPi.GPIO as GPIO
import time


class light:
    def __init__(self, name, pin):
        self.pin = pin
        self.name = name
        self.is_on = False

    def switch_light(self):
        self.is_on = not self.is_on
        if self.is_on:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)


def run_light_loop(pipe,light, delay, callback, stop_event):
    while True:
        message = pipe.recv()
        message = str(message).strip().lower()
        if message == "l":
            light_state = not light_state
            light.switch_light()
        callback(light.is_on, light.name)
        if stop_event.is_set():
            break
        time.sleep(delay)
