import RPi.GPIO as GPIO


class Button:
    def __init__(self, pin, name):
        self.pin = int(pin)
        self.name = name
        GPIO.setup(self.pin, GPIO.OUT)


def run_button_loop(button, button_pressed, button_released, stop_event, publish_event, settings):
    GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback=lambda channel: button_pressed(publish_event, settings),
                          bouncetime=100)
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(button.pin)
            break
