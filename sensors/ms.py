import time

import RPi.GPIO as GPIO


class MS:

    def __init__(self, settings):
        self.R1 = settings["R1"]
        self.R2 = settings["R2"]
        self.R3 = settings["R3"]
        self.R4 = settings["R4"]
        self.C1 = settings["C1"]
        self.C2 = settings["C2"]
        self.C3 = settings["C3"]
        self.C4 = settings["C4"]
        self.name = settings["name"]
        self.pass_code = ""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_char(self, line, characters):
        current_key = ""
        GPIO.output(line, GPIO.HIGH)
        if (GPIO.input(self.C1) == 1):
            current_key = characters[0]
        if (GPIO.input(self.C2) == 1):
            current_key = characters[1]
        if (GPIO.input(self.C3) == 1):
            current_key = characters[2]
        if (GPIO.input(self.C4) == 1):
            current_key = characters[3]
        GPIO.output(line, GPIO.LOW)
        if current_key != "":
            print(current_key)
            self.pass_code += current_key
            print(self.pass_code)

    def get_pass(self):
        self.read_char(self.R1, ["1", "2", "3", "A"])
        self.read_char(self.R2, ["4", "5", "6", "B"])
        self.read_char(self.R3, ["7", "8", "9", "C"])
        self.read_char(self.R4, ["*", "0", "#", "D"])
        return self.pass_code


def run_ms_loop(ms, delay, callback, stop_event):
    while True:
        passcode = ms.get_pass()
        callback(passcode, ms.name)
        if stop_event.is_set():
            break
        time.sleep(delay)  # Delay between readings
