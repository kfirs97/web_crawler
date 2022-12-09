from selenium.webdriver.common.by import By


# ### Match Report page functions ###
# get the stats from match report page
def get_game_stats(driver, url):
    parameters = ['Total', 'Open Play', 'Set Piece', 'Counter Attack', 'Penalty', 'Own Goal', 'Shots', 'Goals',
                  'Conversion Rate']
    team1_params = []
    team2_params = []
    driver.get(url)
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.CLASS_NAME, 'stat')
    for i in range(len(elements)):
        stats = elements[i].text.split(parameters[i])
        team1_params.append(stats[0])
        team2_params.append(stats[1])
    print(team1_params)
    print(team2_params)


# ### League Fixtures page functions ###
# get match reports links from fixtures page
def get_page_match_reports(driver):
    match_reports = []
    driver.implicitly_wait(2)
    try:
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.text == 'Match Report':
                match_reports.append(element.get_attribute('href'))
        print(len(match_reports))
        print(match_reports)
    except:
        print('trying again...')
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.text == 'Match Report':
                match_reports.append(element.get_attribute('href'))
        print(len(match_reports))
        print(match_reports)

    return match_reports


# go to the previous page inside league fixtures page
def get_prev_page(driver):
    try:
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.get_attribute('title') == 'View previous week':
                element.click()
                driver.implicitly_wait(2)
                return True
        return False
    except Exception as e:
        print('exception')
        return True


# ### Entire Season functions
# get whole season games data
def get_season_data(driver):
    num_of_prevs = 1
    driver.implicitly_wait(2)
    reports = get_page_match_reports()
    for rep in reports:
        get_game_stats(rep)
    for i in range(len(reports)):
        driver.back()

    while get_prev_page():
        reports = get_page_match_reports()
        for rep in reports:
            get_game_stats(rep)
        for i in range(len(reports)):
            driver.back()

        for i in range(num_of_prevs):
            get_prev_page()
        num_of_prevs += 1
