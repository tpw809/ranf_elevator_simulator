from influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "your-token"
INFLUX_ORG = "your-org"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

query_api = client.query_api()

# get data from last hour:
# query = """
# from(bucket: "telemetry")
#   |> range(start: -1h)
#   |> filter(fn: (r) => r._measurement == "environment")
# """
# 
# tables = query_api.query(query)
# 
# for table in tables:
#     for record in table.records:
#         print(
#             f"time={record.get_time()}, "
#             f"field={record.get_field()}, "
#             f"value={record.get_value()}"
#         )

# get most recent data:
query = """
from(bucket: "telemetry")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "environment")
  |> filter(fn: (r) => r._field == "temperature")
  |> last()
"""

result = query_api.query(query)

for table in result:
    for record in table.records:
        print(
            f"Latest temperature: {record.get_value()} "
            f"at {record.get_time()}"
        )


client.close()
