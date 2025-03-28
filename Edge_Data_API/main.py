from influxdb_client import InfluxDBClient
import os

# Set up InfluxDB Client
token = os.environ.get("INFLUXDB_TOKEN")
org = "nhl-edge"
url = "http://localhost:8086"
bucket = "nhl-edge-data"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Flux query to get data from today's date onward
query = '''
from(bucket: "nhl-edge-data")
  |> range(start: today())  // Get data from the start of today
  |> filter(fn: (r) => r._measurement == "player_stats")
'''

# Execute query
tables = query_api.query(query)

# Process the result
for table in tables:
    for record in table.records:
        print(f"Time: {record['_time']}, Player: {record['firstName']} {record['lastName']}, Team: {record['team']}, Position: {record['position']}")
