import os
import time
import requests

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-000008be5880/w1_slave'

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        payload = {'temp_celsius': temp_c, 'temp_fahrenheit': temp_f}
        return payload

while True:
        try:
            r = requests.post('http://things.ubidots.com/api/v1.6/devices/temperature/?token=A1E-yUes0YXv0jZPP3TfMUVtnsL8WPOZU3', data=read_temp())
            print('Posting temperatures in Ubidots')
            print(read_temp())
        except:
            pass          
        time.sleep(10)