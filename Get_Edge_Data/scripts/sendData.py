import json
from pymongo import MongoClient

def add_data_to_mongodb():
    # MongoDB connection
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['nhl_edge']  # Replace 'your_database' with your MongoDB database name
    teams_collection = db['teams']  # Replace 'teams' with the name of your collection containing teams data
    players_collection = db['players']  # Replace 'players' with the name of your collection containing players data

    # Load team data from JSON file
    with open("data/teams.json", "r") as teams_file:
        teams_data = json.load(teams_file)

    with open("data/scraped_data.json", "r") as players_file:
        players_data = json.load(players_file)

    # Insert teams data into MongoDB collection
    teams_collection.insert_many(teams_data)
    print("Teams data has been inserted into MongoDB")

    # Insert teams data into MongoDB collection
    players_collection.insert_many(players_data)
    print("Teams data has been inserted into MongoDB")

add_data_to_mongodb()