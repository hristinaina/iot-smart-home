import threading
import time
from simulators.lcd import run_lcd_simulator

def lcd_callback(humidity, temperature, lcd_settings):
        t = time.localtime()
        print("=" * 10 + lcd_settings["name"] + "=" * 10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")


def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        lcd_thread = threading.Thread(target=run_lcd_simulator, args=(2, lcd_callback, stop_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.LCD.lcd import run_lcd_loop, create_lcd_and_adapter
        print("Starting {} loop".format(settings["name"]))
        LCD, mcp = create_lcd_and_adapter(settings)
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(LCD, mcp, 2, lcd_callback, stop_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        print("{} loop started".format(settings["name"]))
