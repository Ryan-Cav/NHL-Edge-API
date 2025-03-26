import json
import time
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def process_player_data(player_data):
    """Worker function to process data for a single player."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(10)
    
    player_id = player_data['id']
    position_code = player_data['positionCode']
    error_xpath = '//*[@id="profile-section"]/div/div[contains(@class, "nhl-404")]'
    team_id = player_data['team']

    url = f'https://edge.nhl.com/en/{ "goalie" if position_code == "G" else "skater" }/{player_id}'
    xpath = f'//*[@id="{"goverview" if position_code == "G" else "overview"}-section-content"]/div[1]/div/table'

    retries = 0
    while retries < 3:
        try:
            driver.get(url)
            time.sleep(5)
            wait = WebDriverWait(driver, 20)
            if driver.find_elements(By.XPATH, error_xpath):
                driver.quit()
                return (player_data, "Page not found (nhl-404)")

            table = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            data = process_table_data(table, player_data)
            driver.quit()
            return (data, None)
        except Exception as e:
            retries += 1
            time.sleep(10)

    driver.quit()
    return (player_data, f"Failed after {retries} retries")

def getEdgeData():
    """Main function to initiate multiprocessing of player data extraction."""
    print("Starting edge data")

    with open('data/teams.json', 'r') as teams_file:
        teams_data = json.load(teams_file)

    all_player_data = []
    error_players = []
    tasks = []

    for team_data in teams_data:
        team_id = team_data['triCode']
        players_file = f'data/{team_id}_players.json'

        with open(players_file, 'r') as pf:
            players_data = json.load(pf)

        for player_data in players_data:
            player_data['team'] = team_id
            tasks.append(player_data)

    with Pool(processes=4) as pool:
        results = pool.map(process_player_data, tasks)

    for player_result, error in results:
        if error:
            error_players.append({'player_data': player_result, 'error': error})
        else:
            all_player_data.append(player_result)

    with open('data/scraped_data.json', 'w') as f:
        json.dump(all_player_data, f, indent=4)

    with open('data/error_players.json', 'w') as f:
        json.dump(error_players, f, indent=4)

    print("Data extraction complete.")

def process_table_data(table, player_data):
    """Extract and process data from the table."""
    rows = table.find_elements(By.XPATH, './tbody/tr')
    data = {}

    for row in rows:
        cells = row.find_elements(By.XPATH, './td|th')
        if len(cells) >= 4:
            parent_key = cells[0].text.strip()
            data[parent_key] = {
                'value': cells[1].text.strip(),
                'league_average': cells[2].text.strip(),
                'percentile': cells[3].text.strip()
            }

    player_data['scraped_data'] = data
    return player_data
