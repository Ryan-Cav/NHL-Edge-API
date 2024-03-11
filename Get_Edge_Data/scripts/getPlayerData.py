import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            output_file_path = f"data/{raw_tricode}_players.json"
            with open(output_file_path, "w") as output_file:
                output_file.write(filtered_data)

            print(f"Data for {team['fullName']} has been written to {output_file_path}")
        else:
            # If the request was not successful, print an error message
            print(f"Failed to retrieve data for {team['fullName']}. Status code:", response.status_code)

    # Write all player data to a single "players.json" file
    with open("data/players.json", "w") as players_file:
        json.dump(all_players, players_file, indent=2)

    print("All player data has been written to players.json")

getPlayerData()

def getEdgeData():
    print("Starting edge data")

    # Load teams data
    with open('data/teams.json', 'r') as teams_file:
        teams_data = json.load(teams_file)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Enable headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Initialize error list
    error_players = []
    all_player_data = []
    # Iterate over teams
    for team_data in teams_data:
        team_id = team_data['triCode']
        players_file = f'data/{team_id}_players.json'

        # Load players data for the current team
        with open(players_file, 'r') as players_file:
            players_data = json.load(players_file)

        # Iterate over players
        for player_data in players_data:
            player_id = player_data['id']
            position_code = player_data['positionCode']

            print(player_data["team"])
            # URL based on position code
            if position_code == 'G':
                url = f'https://edge.nhl.com/en/goalie/{player_id}'
                xpath = '//*[@id="goverview-section-content"]/div[1]/div/table'
            else:
                url = f'https://edge.nhl.com/en/skater/{player_id}'
                xpath = '//*[@id="overview-section-content"]/div[1]/div/table'

            # Retry loop
            retries = 0
            while retries < 3:
                try:
                    # Navigate to player's URL
                    driver.get(url)

                    # Sleep to ensure page loads properly
                    time.sleep(5)

                    # Wait for table to be visible
                    wait = WebDriverWait(driver, 20)
                    table = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

                    # Extract and process table data
                    # Inside the loop where you process each player's data:
                    all_player_data.append(process_table_data(table, player_data))

                    # Break out of the retry loop if successful
                    break
                except Exception as e:
                    print(f"Error processing player {player_id}: {str(e)}")
                    retries += 1
                    print(f"Retrying ({retries}/3)...")
                    time.sleep(10)  # Wait before retrying

            # If retries exceeded, add player to error list
            if retries == 3:
                error_players.append(player_data)

    # Write error players data to the error file
    with open('data/error_players.json', 'w') as f:
        json.dump(error_players, f, indent=4)

    # Write updated player data back to the JSON file
    with open('data/scraped_data.json', 'w') as f:
        json.dump(all_player_data, f, indent=4)
        f.write('\n')
    # Close the WebDriver
    driver.quit()

def process_table_data(table, player_data):
    # Extract table rows
    rows = table.find_elements(By.XPATH, './tbody/tr')

    # Initialize data dictionary
    data = {}

    # Iterate over rows
    for row in rows:
        # Extract cell values
        cells = row.find_elements(By.XPATH, './td|th')
        parent_key = cells[0].text.strip()
        LA_key = 'League Average'
        perc_key = 'Percentile'
        data[parent_key] = cells[1].text.strip()
        data[LA_key] = cells[2].text.strip()
        data[perc_key] = cells[3].text.strip()

    # Append scraped data to player's data
    player_data['scraped_data'] = data

    return player_data

getEdgeData()