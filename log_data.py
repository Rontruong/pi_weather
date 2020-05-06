from sense_hat import SenseHat
from datetime import datetime
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

import gpiozero as gpio
import subprocess
import re

LAST_MAX = 0
LAST_MIN = 0

def cpu_temp_helper():
    cpu = gpio.CPUTemperature(min_temp=50, max_temp=90)
    return cpu.temperature

def load_avg_helper():
    la = gpio.LoadAverage(min_load_average=0, max_load_average=2)
    return la.load_average

def ping_google():
    global LAST_MAX, LAST_MIN
    p = subprocess.Popen(["ping", "-c", "5","www.google.com"], stdout = subprocess.PIPE)
    resp = p.communicate()[0]
    pattern = 'min\/avg\/max\/mdev = ([0-9]*\.[0-9]*)\/([0-9]*\.[0-9]*)\/([0-9]*\.[0-9]*)\/([0-9]*\.[0-9]*)'
    mmin, aavg, mmax, mmdev = re.findall(pattern, str(resp))[0]
    LAST_MAX = mmax
    LAST_MIN = mmin
    return aavg

def get_last_max():
    global LAST_MAX
    return LAST_MAX
def get_last_min():
    global LAST_MIN
    return LAST_MIN

sense = SenseHat()
csv_file = '/home/pi/pi_weather_station/data.csv'
# hdf_file = '/home/pi/pi_weather_station/data.h5'
data_getters = {'timestamp': datetime.now,
                'temp_humidity_c': sense.get_temperature_from_humidity,
                'temp_pressure_c': sense.get_temperature_from_pressure,
                'humidty_rh': sense.get_humidity,
                'pressure_mbar': sense.get_pressure,
                'cpu_temp_c': cpu_temp_helper,
                'load_avg_percent': load_avg_helper,
                'avg_ping_google_ms': ping_google,
                'min_ping_google_ms': get_last_min,
                'max_ping_google_ms': get_last_max}

data = {}
for k, getter in data_getters.items():
    data[k] = [getter()]

df = pd.DataFrame(data)
# if os.path.isfile(csv_file):
#     df.to_csv(csv_file, mode='a', header=False, index=False, float_format='%.2f')
#     # df.to_hdf(hdf_file, key='table', format='table', append=True, index=False)
# else:
#     df.to_csv(csv_file, index=False, float_format='%.2f')
#     # df.to_hdf(hdf_file, key='table', format='table', index=False)

conn = psycopg2.connect(dbname='')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
sql = "INSERT INTO periodic (timestamp, temp_humidity_c, temp_pressure_c, humidty_rh, pressure_mbar, cpu_temp_c, load_avg_percent,avg_ping_google_ms, min_ping_google_ms,max_ping_google_ms) VALUES %s"
execute_values(cur, sql, df.values)
