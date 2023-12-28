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


def run_buzzer_simulator(delay, callback_activated, callback_deactivated, stop_event, publish_event, settings):
    callback_activated(publish_event, settings)
    while True:
        play_sound(delay)
        if stop_event.is_set():
            callback_deactivated(publish_event, settings)
            break
        time.sleep(delay)
