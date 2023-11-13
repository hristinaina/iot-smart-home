import time


def play_sound(delay):
    try:
        import winsound
    except ImportError:
        import os
        def playsound(frequency, duration):
            os.system('beep -f %s -l %s' % (frequency, duration))
    else:
        def playsound(frequency, duration):
            winsound.Beep(frequency, duration)

    frequency = 1000
    playsound(frequency, delay * 100)


def run_buzzer_simulator(delay, callback_activated, callback_deactivated, name, stop_event):
    callback_activated(name)
    while True:
        play_sound(delay)
        if stop_event.is_set():
            callback_deactivated(name)
            break
        time.sleep(delay)
