import time

import RPi.GPIO as GPIO

class B4SD:
    def __init__(self, settings):
        # GPIO ports for the 7seg pins
        self.segments = settings["segments"]
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        # GPIO ports for the digit 0-3 pins
        self.digits = settings["digits"]
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

        self.name = settings["name"]
        self.num = {' ': (0, 0, 0, 0, 0, 0, 0),
               '0': (1, 1, 1, 1, 1, 1, 0),
               '1': (0, 1, 1, 0, 0, 0, 0),
               '2': (1, 1, 0, 1, 1, 0, 1),
               '3': (1, 1, 1, 1, 0, 0, 1),
               '4': (0, 1, 1, 0, 0, 1, 1),
               '5': (1, 0, 1, 1, 0, 1, 1),
               '6': (1, 0, 1, 1, 1, 1, 1),
               '7': (1, 1, 1, 0, 0, 0, 0),
               '8': (1, 1, 1, 1, 1, 1, 1),
               '9': (1, 1, 1, 1, 0, 1, 1)}

    def show_value(self):
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0, 7):
                GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)
        return "{}:{}".format(n[0:2], n[2:])


def run_b4sd_loop(b4sd, delay, callback, stop_event, settings):
    while True:
        value = b4sd.show_value()
        callback(value, settings)
        if stop_event.is_set():
            GPIO.cleanup()
            break
