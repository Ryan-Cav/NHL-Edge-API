from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient('mongodb://mongodb:27017/')

db = client['your_database']  # Replace 'your_database' with your MongoDB database name
players_collection = db['players']  # Replace 'players' with the name of your collection containing players data
teams_collection = db['teams']  # Replace 'teams' with the name of your collection containing teams data

@app.get("/")
def read_root():
    return {
        "docs": {
            "github": "https://github.com/Ryan-Cav/NHL-Edge-API",
            "nhl-edge": "https://edge.nhl.com/en/home"
        }
    }

@app.get("/teams/")
def all_teams():
    # Fetch all teams from the MongoDB collection
    teams_data = list(teams_collection.find())
    return teams_data

@app.get("/teams/{team_id}")
def get_team(team_id: int):
    # Search for the team with the given ID in the MongoDB collection
    team = teams_collection.find_one({"id": team_id})
    if team:
        return team
    else:
        raise HTTPException(status_code=404, detail="Team not found")

@app.get("/players/")
def all_players():
    # Fetch all players from the MongoDB collection
    players_data = list(players_collection.find())
    return players_data

@app.get("/players/{player_id}")
def get_player(player_id: int):
    # Search for the player with the given ID in the MongoDB collection
    player = players_collection.find_one({"id": player_id})
    if player:
        return player
    else:
        raise HTTPException(status_code=404, detail="Player not found")
