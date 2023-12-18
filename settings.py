import json
import threading

HOSTNAME = "localhost"
PORT = 1883


def load_settings(filePath='settings1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)


lock = threading.Lock()
