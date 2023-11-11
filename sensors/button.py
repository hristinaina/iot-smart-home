import RPi.GPIO as GPIO


class Button:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name


def run_button_loop(button, button_pressed, button_released, stop_event):
    GPIO.setup(button.pin, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback=lambda channel: button_pressed(button.name), bouncetime=100)
    GPIO.add_event_detect(button.pin, GPIO.FALLING, callback=lambda channel: button_released(button.name), bouncetime=100)
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(button.pin)
            break
