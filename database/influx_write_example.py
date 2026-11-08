# Needs an influx server running!!! (did not do yet)
# pip install influxdb-client
import time
import numpy as np
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision

# Create the standard numpy generator object
rng = np.random.default_rng()

# InfluxDB settings:
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "your-token"
INFLUX_ORG = "your-org"
INFLUX_BUCKET = "telemetry"  # name of data bucket

WRITE_INTERVAL_SECONDS = 10

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api()

try:
    while True:
        # Simulated measurement / dynamics:
        temperature = np.round(rng.uniform(20.0, 30.0), 3)
        humidity = np.round(rng.uniform(40.0, 60.0), 3)

        point = (
            Point("environment")
            .tag("location", "lab")
            .field("temperature", temperature)
            .field("humidity", humidity)
            .time(datetime.utcnow(), WritePrecision.NS)
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            record=point
        )

        print(
            f"[{datetime.utcnow()}] "
            f"temperature={temperature} "
            f"humidity={humidity}"
        )

        time.sleep(WRITE_INTERVAL_SECONDS)


except KeyboardInterrupt:
    print("Stopping writer...")

finally:
    client.close()
    