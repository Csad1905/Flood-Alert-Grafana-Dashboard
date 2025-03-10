"""
Data generator for the Flooding Data project.
"""
import random
import time
from datetime import datetime
from pymongo import MongoClient
from faker import Faker

# Initialize Faker
fake = Faker()

# MongoDB connection string (assuming local MongoDB instance)
client = MongoClient("mongodb://localhost:27017/")
db = client["Flooding-Data"]

# Collections
rainfall_collection = db["Rainfall-data"]
sea_level_collection = db["Sea-level-data"]
river_level_collection = db["River-level-data"]

# List of cities in Suffolk, Norfolk, and Essex to ensure
# data is generated for these locations.
locations = [
    # Suffolk
    "Ipswich", "Bury St Edmunds", "Lowestoft", "Felixstowe", "Stowmarket",
    "Sudbury", "Haverhill", "Mildenhall", "Newmarket", "Saxmundham",
    "Woodbridge", "Kesgrave", "Rushmere St. Andrew", "East Ipswich",
    # Norfolk
    "Norwich", "Great Yarmouth", "King's Lynn", "Thetford", "Dereham",
    "Cromer", "Wells-next-the-Sea", "Aylsham", "Holt", "Fakenham",
    "Attleborough", "Watton", "Swaffham", "Diss",
    # Essex
    "Colchester", "Chelmsford", "Southend-on-Sea", "Basildon", "Harlow",
    "Clacton-on-Sea", "Braintree", "Maldon", "Harwich", "Frinton-on-Sea",
    "Saffron Walden", "Epping", "Rayleigh", "Wickford", "Thundersley"
]

# List of seaside towns
seaside_towns = [
    "Lowestoft", "Felixstowe", "Southend-on-Sea",
    "Great Yarmouth", "King's Lynn",
    "Cromer", "Wells-next-the-Sea", "Clacton-on-Sea",
    "Harwich", "Frinton-on-Sea"
]

# List of river towns (locations near rivers)
river_towns = [
    "Ipswich", "Bury St Edmunds", "Stowmarket",
    "Sudbury", "Haverhill", "Mildenhall",
    "Saxmundham", "Woodbridge", "Kesgrave",
    "Norwich", "Attleborough", "Dereham",
    "Aylsham", "Holt", "Fakenham", "Watton",
    "Swaffham", "Diss", "Colchester",
    "Chelmsford", "Basildon", "Braintree", "Saffron Walden",
    "Epping", "Rayleigh", "Wickford", "Thundersley"
]


def generate_rainfall_data():
    """
    Generate fake rainfall data.
    """
    return {
        "station_id": fake.uuid4(),
        "location": random.choice(locations),
        "timestamp": datetime.utcnow().isoformat(),
        # Random rainfall between 0 and 10 mm
        "rainfall_mm": random.uniform(0, 10)
    }


def generate_sea_level_data():
    """
    Generate fake sea level data only for seaside towns.
    """
    location = random.choice(seaside_towns)
    return {
        "station_id": fake.uuid4(),
        "location": location,
        "timestamp": datetime.utcnow().isoformat(),
        # Sea level between 1 and 3 meters
        "sea_level_m": round(random.uniform(1.0, 3.0), 1)
    }


def generate_river_level_data():
    """
    Generate fake river level data only for river towns.
    """
    location = random.choice(river_towns)
    return {
        "station_id": fake.uuid4(),
        "location": location,
        "timestamp": datetime.utcnow().isoformat(),
        # River level between 2 and 5 meters
        "river_level_m": round(random.uniform(2.0, 5.0), 1)
    }


def insert_data():
    """
    Generate and insert data into MongoDB collections.
    """
    rainfall_data = generate_rainfall_data()

    # Sea level data is only generated for seaside towns.
    sea_level_data = generate_sea_level_data()

    # River level data is only generated for river towns.
    river_level_data = generate_river_level_data()

    # Insert into collections
    rainfall_collection.insert_one(rainfall_data)
    sea_level_collection.insert_one(sea_level_data)
    river_level_collection.insert_one(river_level_data)

    print(f"Inserted data at {rainfall_data['timestamp']}")
    print(f"Rainfall: {rainfall_data['rainfall_mm']} mm")
    print(f"Sea Level: {sea_level_data['sea_level_m']} m")
    print(f"River Level: {river_level_data['river_level_m']} m")
    print("-" * 40)


# Generate and insert data every 10 seconds
while True:
    insert_data()
    time.sleep(10)  # Wait for 10 seconds before inserting new data
