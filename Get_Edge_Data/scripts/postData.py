import json
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "nhl-edge"
url = "http://localhost:8086"

def postData():
    client = InfluxDBClient(url=url, token=token, org=org)

    bucket = "nhl-edge-data"
    write_api = client.write_api(write_options=SYNCHRONOUS)

    with open('data/results/scraped_data.json', 'r') as pf:
        players_edge_data = json.load(pf)

    points = []
    
    # Get league averages from the first goalie and first skater
    first_goalie = None
    first_skater = None

    for player in players_edge_data:
        if player["positionCode"] == "G" and first_goalie is None:
            first_goalie = player
        elif player["positionCode"] != "G" and first_skater is None:
            first_skater = player
        
        # Stop once both first goalie and skater are found
        if first_goalie and first_skater:
            break

    # Set league averages based on the first goalie and first skater's data
    league_averages = {}

    if first_goalie:
        stats = first_goalie["scraped_data"]
        league_averages["G"] = {
            "gaa": safe_float(stats["GAA"]["value"]),
            "overallSavePercentage": safe_float(stats["Overall Save %"]["value"]),
            "highDangerSavePercentage": safe_float(stats["High Danger Save %"]["value"]),
            "midRangeSavePercentage": safe_float(stats["Mid-Range Save %"]["value"]),
            "pctGamesAbove900": safe_float(stats["Pct. Games > .900"]["value"]),
            "goalDiffPer60": safe_float(stats["Goal Diff. Per 60"]["value"]),
            "goalsForAverage": safe_float(stats["Goals For Average"]["value"]),
            "pointsPercentage": safe_float(stats["Points %"]["value"])
        }

    if first_skater:
        stats = first_skater["scraped_data"]
        league_averages["S"] = {
            "topSkatingSpeed": safe_float(stats["Top Skating Speed (mph)"]["value"]),
            "speedBurstsOver20mph": safe_float(stats["Speed Bursts Over 20 mph"]["value"]),
            "skatingDistance": safe_float(stats["Skating Distance (mi)"]["value"]),
            "topShotSpeed": safe_float(stats["Top Shot Speed (mph)"]["value"]),
            "shotsOnGoal": safe_float(stats["Shots on Goal"]["value"]),
            "shootingPercentage": safe_float(stats["Shooting %"]["value"].replace("%", "")),
            "goals": safe_float(stats["Goals"]["value"]),
            "offensiveZoneTime": safe_float(stats["Off. Zone Time (ES)"]["value"].replace("%", ""))
        }

    # Write league averages to the database
    if first_goalie:
        point = Point("league_averages") \
            .tag("position", "G")
        for stat, avg_value in league_averages["G"].items():
            point = point.field(stat, avg_value)
        points.append(point)

    if first_skater:
        point = Point("league_averages") \
            .tag("position", "S")
        for stat, avg_value in league_averages["S"].items():
            point = point.field(stat, avg_value)
        points.append(point)

    # Write player data
    for player in players_edge_data:
        point = Point("player_stats") \
            .tag("id", str(player["id"])) \
            .tag("team", player["team"]) \
            .tag("position", player["positionCode"]) \
            .field("firstName", player["firstName"]) \
            .field("lastName", player["lastName"]) \
            .field("sweaterNumber", int(player["sweaterNumber"])) \
            .field("shootsCatches", player["shootsCatches"]) \
            .field("heightInInches", int(player["heightInInches"])) \
            .field("weightInPounds", int(player["weightInPounds"])) \
            .field("heightInCentimeters", int(player["heightInCentimeters"])) \
            .field("weightInKilograms", int(player["weightInKilograms"])) \
            .field("birthDate", player["birthDate"]) \
            .field("birthCity", player["birthCity"]) \
            .field("birthCountry", player["birthCountry"]) \
            .field("birthStateProvince", player["birthStateProvince"])

        stats = player["scraped_data"]

        # Goalie-Specific Fields
        if player["positionCode"] == "G":
            point = point.field("gaa", safe_float(stats["GAA"]["value"])) \
                        .field("overallSavePercentage", safe_float(stats["Overall Save %"]["value"])) \
                        .field("highDangerSavePercentage", safe_float(stats["High Danger Save %"]["value"])) \
                        .field("midRangeSavePercentage", safe_float(stats["Mid-Range Save %"]["value"])) \
                        .field("pctGamesAbove900", safe_float(stats["Pct. Games > .900"]["value"])) \
                        .field("goalDiffPer60", safe_float(stats["Goal Diff. Per 60"]["value"])) \
                        .field("goalsForAverage", safe_float(stats["Goals For Average"]["value"])) \
                        .field("pointsPercentage", safe_float(stats["Points %"]["value"]))
        
        # Skater and Defenseman Fields (Shared)
        else:
            point = point.field("topSkatingSpeed", safe_float(stats["Top Skating Speed (mph)"]["value"])) \
                        .field("speedBurstsOver20mph", int(stats["Speed Bursts Over 20 mph"]["value"])) \
                        .field("skatingDistance", safe_float(stats["Skating Distance (mi)"]["value"])) \
                        .field("topShotSpeed", safe_float(stats["Top Shot Speed (mph)"]["value"])) \
                        .field("shotsOnGoal", int(stats["Shots on Goal"]["value"])) \
                        .field("shootingPercentage", safe_float(stats["Shooting %"]["value"].replace("%", ""))) \
                        .field("goals", int(stats["Goals"]["value"])) \
                        .field("offensiveZoneTime", safe_float(stats["Off. Zone Time (ES)"]["value"].replace("%", "")))

        points.append(point)

    write_api.write(bucket=bucket, org="nhl-edge", record=points)

    print("Bulk write completed successfully!")
    client.close()

def safe_float(value):
    return float(value) if value not in ["-", ""] else None

postData()