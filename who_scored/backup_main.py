from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from debug.Debug import Debug


# ### Match Report page functions ###
# get the stats from match report page
def get_game_stats(url):
    # initialize the parameters names
    parameters = ['Total', 'Open Play', 'Set Piece', 'Counter Attack', 'Penalty', 'Own Goal', 'Shots', 'Goals',
                  'Conversion Rate']
    # initialize list for each team
    team1_params = []
    team2_params = []
    # go to the match report page
    driver.get(url)
    driver.implicitly_wait(3)
    # pull the stat elements
    elements = driver.find_elements(By.CLASS_NAME, 'stat')
    for i in range(len(elements)):
        # split the text by the relevant parameters to get the data of each team
        stats = elements[i].text.split(parameters[i])
        team1_params.append(stats[0])
        team2_params.append(stats[1])
    Debug.log(team1_params)
    Debug.log(team2_params)


# get the names of the teams that played
def get_team_names():
    elements = driver.find_elements(By.CLASS_NAME, 'team-link')
    teams = []
    for element in elements:
        if element.text:
            teams.append(element.text)
    return teams


# get details about the game (half-time score, full-time score, kick off time, game date)
def get_game_details():
    elements = driver.find_elements(By.TAG_NAME, 'dl')
    game_details = {}
    for i in range(1, 3):
        data = elements[i].text.split('\n')
        game_details[data[0]] = data[1]
        game_details[data[2]] = data[3]
    return game_details


# ### League Fixtures page functions ###
# get match reports links from fixtures page
def get_page_match_reports():
    # init a list for the match reports urls
    match_reports = []
    driver.implicitly_wait(2)
    try:
        # fund the relevant elements and add them to the list
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.text == 'Match Report':
                match_reports.append(element.get_attribute('href'))
        Debug.log(len(match_reports))
        Debug.log(match_reports)
    except:
        # try the same process again because exception can become when the DOM change and code tries to retreive data
        # from an old element
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.text == 'Match Report':
                match_reports.append(element.get_attribute('href'))
        Debug.log(len(match_reports))
        Debug.log(match_reports)

    return match_reports


# go to the previous page inside league fixtures page
def get_prev_page():
    try:
        # find the previous week button and click it, return true if succeeded (if not, it's probably the first page)
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.get_attribute('title') == 'View previous week':
                element.click()
                driver.implicitly_wait(2)
                return True
        return False
    except Exception as e:
        print('exception')


# ### Entire Season functions
# get whole season games data
def get_season_data():
    base_url = driver.current_url  # save the url for the started page
    num_of_prevs = 1  # fixing a website bug, the site always return us to the first page

    reports = get_page_match_reports()  # get the match report links from the current page
    # get the stats from each match report
    for rep in reports:
        get_game_stats(rep)

    # go back to the League Fixtures page
    driver.get(base_url)

    while get_prev_page():
        # repeat the process until we finish the year's games
        reports = get_page_match_reports()
        for rep in reports:
            get_game_stats(rep)

        driver.get(base_url)

        for i in range(num_of_prevs):
            get_prev_page()
        num_of_prevs += 1


def main():
    reports = get_page_match_reports(
        'https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/8618/England-Premier-League')
    for rep in reports:
        get_game_stats(rep)
    # get_game_stats(ARSENAL_VS_BRANTFORD)
    driver.close()


def test():
    driver.implicitly_wait(2)
    get_prev_page()
    try:
        kfir = get_page_match_reports()
    except Exception as e:
        print(str(e))


PATH = 'C:\kfir\Projects\chrome_webdriver\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://www.whoscored.com/Matches/1549904/Show/England-Premier-League-2021-2022-Newcastle-Arsenal')
driver.implicitly_wait(2)
element = driver.find_element(By.ID, 'previous-meetings-container')
print(element)
print(element.text)
print(len(element.text.split('\n')))
data = element.text.split('\n')

games = {
    # 'game1': {
    #     'tournament': '',
    #     'date': '',
    #     'home team name': '',
    #     'home team score': '',
    #     'away team name': '',
    #     'away team score': ''
    # }
}
for i in range(11, len(data)):
    games[f'game{i-10}'] = {}
    games[f'game{i-10}']['tournament'] = data[i]
    games[f'game{i-10}']['date'] = data[i+1]
    score_stats = data[i+2].split(':')
    print(score_stats[0])
    print(score_stats[1])
    score_stats[0] = score_stats[0].strip()
    score_stats[1] = score_stats[1].strip()
    games[f'game{i-10}']['home team score'] = score_stats[0][-1]
    games[f'game{i-10}']['home team name'] = score_stats[0][0:len(score_stats[0])-1]
    games[f'game{i-10}']['away team score'] = score_stats[1][0]
    games[f'game{i-10}']['away team name'] = score_stats[0][1:len(score_stats[0])]
ס;
print(games)



driver.close()
