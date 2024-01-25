#!/usr/bin/env python3
import MPU6050 
import time
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json


accel = [0]*3               #store accelerometer data
gyro = [0]*3                #store gyroscope data


def run_gyro_loop(mpu, delay, callback, stop_event, publish_event, settings):
    mpu.dmp_initialize()
    while True:
        accel = mpu.get_acceleration()      #get accelerometer data
        gyro = mpu.get_rotation()           #get gyroscope data
        accel = [a/16384.0 for a in accel]
        gyro = [g/131.0 for g in gyro]
        callback(accel, gyro, publish_event, settings)
        os.system('clear')
        if stop_event.is_set():
            break
        time.sleep(delay)


