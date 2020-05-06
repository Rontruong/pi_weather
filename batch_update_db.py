from dateutil.parser import parse
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(dbname='')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
df = pd.read_csv('data.csv', parse_dates=['timestamp'], date_parser=parse)

sql = "INSERT INTO periodic (timestamp, temp_humidity_c, temp_pressure_c, humidty_rh, pressure_mbar, cpu_temp_c, load_avg_percent,avg_ping_google_ms, min_ping_google_ms,max_ping_google_ms) VALUES %s"
execute_values(cur, sql, df.values)
