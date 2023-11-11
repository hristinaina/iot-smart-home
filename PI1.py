
import threading

from components.uds import run_uds
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.button import run_button
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        dht1_settings = settings['DHT1']
        dht2_settings = settings['DHT2']
        uds1_settings = settings['DUS1']
        rpir1_settings = settings['RPIR1']
        rpir2_settings = settings['RPIR2']
        dpir1_settings = settings['DPIR1']
        ds1_settings = settings['DS1']
        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)
        run_uds(uds1_settings, threads, stop_event)
        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)
        run_button(ds1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
