from datetime import datetime, timedelta, timezone

import influxdb_client

org = "org"
token = "<token>"
url = "http://localhost:8086/"

clientProd = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org,
    timeout=40000,
)

query_api = clientProd.query_api()

timezone_offset = 0.0  # (UTC−03:00)
tzinfo = timezone(timedelta(hours=timezone_offset))
start = datetime(2023, 1, 30, tzinfo=tzinfo)
stop = datetime(2024, 2, 28, tzinfo=tzinfo)

print(f"Querying period: {start.isoformat()} to {stop.isoformat()}")

query = f' from(bucket: "default")\
    |> range(start: {start.isoformat()}, stop: {stop.isoformat()})\
    |> filter(fn: (r) => r["_measurement"] == "cbor_sensors")\
    |> filter(fn: (r) => r["_field"] == "sensors_data")'

query_result = query_api.query_raw(org=org, query=query)
data = query_result.read()
print(f"Returned `{data}`")
