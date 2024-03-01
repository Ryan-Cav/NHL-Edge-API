import json
import requests


def getPlayerData():
    # Load team data from JSON file
    with open("../data/teams.json", "r") as teams_file:
        teams = json.load(teams_file)

    # Define the base endpoint URL
    base_endpoint = "https://api-web.nhle.com/v1/roster/"

    # List to store player data for all teams
    all_players = []

    # Iterate over each team
    for team in teams:
        # Extract the rawTricode for the team
        raw_tricode = team["rawTricode"]
        
        # Construct the endpoint URL for the team
        endpoint = f"{base_endpoint}{raw_tricode}/20232024"

        # Send a GET request to the endpoint
        response = requests.get(endpoint)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the JSON data from the response
            data = response.json()

            # Extracting player information
            players = []
            for category in data.values():
                for player in category:
                    players.append(player)

            # Convert to JSON format with the desired structure
            formatted_players = []
            for player in players:
                formatted_player = {
                    "id": player.get("id", ""),
                    "headshot": player.get("headshot", ""),
                    "firstName": player.get("firstName", {}).get("default", ""),
                    "lastName": player.get("lastName", {}).get("default", ""),
                    "sweaterNumber": player.get("sweaterNumber", ""),  # Use .get() to handle missing key
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
                    "team": team["fullName"]  # Add the team name to distinguish players
                }
                formatted_players.append(formatted_player)

            # Extend the list of all players with the formatted players for this team
            all_players.extend(formatted_players)

            # Convert the formatted data to JSON format
            filtered_data = json.dumps(formatted_players, indent=2)

            # Write the filtered data to a new JSON file for each team
            output_file_path = f"../data/{raw_tricode}_players.json"
            with open(output_file_path, "w") as output_file:
                output_file.write(filtered_data)

            print(f"Data for {team['fullName']} has been written to {output_file_path}")
        else:
            # If the request was not successful, print an error message
            print(f"Failed to retrieve data for {team['fullName']}. Status code:", response.status_code)

    # Write all player data to a single "players.json" file
    with open("../data/players.json", "w") as players_file:
        json.dump(all_players, players_file, indent=2)

    print("All player data has been written to players.json")