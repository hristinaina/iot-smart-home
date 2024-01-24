import time


def run_light_simulator(pipe, delay, callback, stop_event, publish_event, settings):
    last_light_time = time.time()
    while True:

        if pipe.poll():
            message = pipe.recv()
            message = str(message).strip().lower()
            if message == "l":
                last_light_time = time.time()

        light_state = time.time() - last_light_time <= 10

        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(light_state, publish_event, settings)
        if stop_event.is_set():
            break