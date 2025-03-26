import json
import requests

def getPlayerData():
    # Load team data from JSON file
    with open("data/teams.json", "r") as teams_file:
        teams = json.load(teams_file)

    # Define the base endpoint URL
    base_endpoint = "https://api-web.nhle.com/v1/roster/"

    # List to store player data for all teams
    all_players = []

    # Iterate over each team
    for team in teams:
        raw_tricode = team["rawTricode"]
        endpoint = f"{base_endpoint}{raw_tricode}/20242025"

        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            players = [player for category in data.values() for player in category]

            formatted_players = []
            for player in players:
                formatted_player = {
                    "id": player.get("id", ""),
                    "headshot": player.get("headshot", ""),
                    "firstName": player.get("firstName", {}).get("default", ""),
                    "lastName": player.get("lastName", {}).get("default", ""),
                    "sweaterNumber": player.get("sweaterNumber", ""),
                    "positionCode": player.get("positionCode", ""),
                    "shootsCatches": player.get("shootsCatches", ""),
                    "heightInInches": player.get("heightInInches", ""),
                    "weightInPounds": player.get("weightInPounds", ""),
                    "heightInCentimeters": player.get("heightInCentimeters", ""),
                    "weightInKilograms": player.get("weightInKilograms", ""),
                    "birthDate": player.get("birthDate", ""),
                    "birthCity": player.get("birthCity", {}).get("default", ""),
                    "birthCountry": player.get("birthCountry", ""),
                    "birthStateProvince": player.get("birthStateProvince", {}).get("default", ""),
                    "team": team["fullName"]
                }
                formatted_players.append(formatted_player)

            all_players.extend(formatted_players)

            output_file_path = f"data/{raw_tricode}_players.json"
            with open(output_file_path, "w") as output_file:
                json.dump(formatted_players, output_file, indent=2)

            print(f"Data for {team['fullName']} has been written to {output_file_path}")
        else:
            print(f"Failed to retrieve data for {team['fullName']}. Status code:", response.status_code)

    with open("data/players.json", "w") as players_file:
        json.dump(all_players, players_file, indent=2)

    print("All player data has been written to players.json")
