import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Load teams data
    with open('../data/teams.json', 'r') as teams_file:
        teams_data = json.load(teams_file)

    # Configure Chrome options
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Enable headless mode

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Initialize error list
    error_players = []
    all_player_data = []
    # Iterate over teams
    for team_data in teams_data:
        team_id = team_data['triCode']
        players_file = f'../data/{team_id}_players.json'

        # Load players data for the current team
        with open(players_file, 'r') as players_file:
            players_data = json.load(players_file)

        # Iterate over players
        for player_data in players_data:
            player_id = player_data['id']
            position_code = player_data['positionCode']

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
    with open('../data/error_players.json', 'w') as f:
        json.dump(error_players, f, indent=4)

    # Write updated player data back to the JSON file
    with open('../data/scraped_data.json', 'a') as f:
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
    

if __name__ == "__main__":
    main()
