CREATE TABLE periodic (
    timestamp           TIMESTAMP,
    temp_humidity_c     NUMERIC,
    temp_pressure_c     NUMERIC,
    humidty_rh          NUMERIC,
    pressure_mbar       NUMERIC,
    cpu_temp_c          NUMERIC,
    load_avg_percent    NUMERIC,
    avg_ping_google_ms  NUMERIC,
    min_ping_google_ms  NUMERIC,
    max_ping_google_ms  NUMERIC
);