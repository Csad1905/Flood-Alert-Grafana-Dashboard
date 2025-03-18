"""
This script connects to a MongoDB database and queries the latest data from
three collections: Rainfall-data, Sea-level-data, and River-level-data.
"""
import time
from prometheus_client import start_http_server, Gauge
from pymongo import MongoClient

# Set up the Prometheus Gauge metrics for rainfall, sea level, and river level
rainfall_gauge = Gauge('rainfall_mm',
                       'Rainfall measurement',
                       ['station_id', 'location'])
sea_level_gauge = Gauge('sea_level_m',
                        'Sea level measurement',
                        ['station_id', 'location'])
river_level_gauge = Gauge('river_level_m',
                          'River level measurement',
                          ['station_id', 'location'])

# Connect to MongoDB using Docker DNS
client = MongoClient(
                        'mongodb://mongodb:27017/'
                    )
db = client['Flooding-Data']

# Collections
rainfall_collection = db['Rainfall-data']
sea_level_collection = db['Sea-level-data']
river_level_collection = db['River-level-data']

# Start the Prometheus HTTP server to expose metrics
start_http_server(8000)

while True:
    # Query MongoDB for the latest data from each collection

    # Get rainfall data
    rainfall_data = rainfall_collection.find()
    for record in rainfall_data:
        station_id = record.get('station_id')
        location = record.get('location')
        rainfall_mm = record.get('rainfall_mm')
        if rainfall_mm is not None:
            rainfall_gauge.labels(station_id=station_id,
                                  location=location).set(rainfall_mm)

    # Get sea level data
    sea_level_data = sea_level_collection.find()
    for record in sea_level_data:
        station_id = record.get('station_id')
        location = record.get('location')
        sea_level = record.get('sea_level_m')
        if sea_level is not None:
            sea_level_gauge.labels(station_id=station_id,
                                   location=location).set(sea_level)

    # Get river level data
    river_level_data = river_level_collection.find()
    for record in river_level_data:
        station_id = record.get('station_id')
        location = record.get('location')
        river_level = record.get('river_level_m')
        if river_level is not None:
            river_level_gauge.labels(station_id=station_id,
                                     location=location).set(river_level)

    time.sleep(10)  # Sleep for 10 seconds before collecting again
