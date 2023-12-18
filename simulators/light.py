import time


def run_light_simulator(pipe, delay, callback, stop_event, publish_event, settings):
    light_state = False
    while True:
        message = pipe.recv()
        message = str(message).strip().lower()
        if message == "l":
            light_state = not light_state
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(light_state, publish_event, settings)
        if stop_event.is_set():
            break
