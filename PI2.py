import multiprocessing
import threading

from components.gyro import run_gyro
from components.lcd import run_lcd
from components.button import run_button
from components.uds import run_uds
from settings import load_settings
from components.dht import run_dht
from components.pir import run_pir

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def menu():
    print("="*10 + "  MENU  " + "="*10)
    print("-- Enter X to stop all devices --")
    print("=" * 30)


if __name__ == "__main__":
    print('Starting PI2')
    menu()
    settings = load_settings('settings2.json')
    threads = []

    stop_event = threading.Event()
    try:
        gdht_settings = settings['GDHT']
        rdht3_settings = settings['RDHT3']
        uds2_settings = settings['DUS2']
        rpir3_settings = settings['RPIR3']
        dpir2_settings = settings['DPIR2']
        glcd_settings = settings['GLCD']
        gsg_settings = settings['GSG']
        ds2_settings = settings['DS2']

        run_dht(gdht_settings, threads, stop_event)
        run_dht(rdht3_settings, threads, stop_event)
        run_uds(uds2_settings, threads, stop_event)
        run_pir(rpir3_settings, threads, stop_event)
        run_pir(dpir2_settings, threads, stop_event)
        run_lcd(glcd_settings, threads, stop_event)
        run_gyro(gsg_settings, threads, stop_event)
        run_button(ds2_settings, threads, stop_event)

        while True:
            user_input = input().strip().upper()
            if user_input == "X":
                stop_event.set()

    except KeyboardInterrupt:
        print('\nStopping app')
        for t in threads:
            stop_event.set()
