from typing import Union

from fastapi import FastAPI, HTTPException

import json
import requests

app = FastAPI()

# Open the players.json file and load its contents
with open("./Data/players.json", "r") as players_file:
    players_data = json.load(players_file)
with open("./Data/teams.json", "r") as teams_file:
    teams_data = json.load(teams_file)

@app.get("/")
def read_root():
    return  {
                "docs": {
                    "github" : "https://github.com/Ryan-Cav/NHL-Edge-API", 
                    "nhl-edge": "https://edge.nhl.com/en/home"
                }
            }

@app.get("/teams/")
def allPlayers():    
    # Return the JSON data
    return teams_data

@app.get("/teams/{team_id}")
def getTeam(team_id: int):
    # Search for the player with the given ID
    for team in teams_data:
        if team["id"] == team_id:
            return team
    # If the player is not found, raise an HTTPException with status code 404
    raise HTTPException(status_code=404, detail="Player not found")

@app.get("/players/")
def allPlayers():    
    # Return the JSON data
    return players_data

@app.get("/players/{player_id}")
def getPlayer(player_id: int):
    # Search for the player with the given ID
    for player in players_data:
        if player["id"] == player_id:
            return player
    # If the player is not found, raise an HTTPException with status code 404
    raise HTTPException(status_code=404, detail="Player not found")