from selenium.webdriver.common.by import By


def get_head_to_head(driver):
    element = driver.find_element(By.CLASS_NAME, 'scorebox')
    data = element.text.split('\n')
    team1 = {'name': data[0], 'wins': data[1].split(' ')[0], 'draws': data[2].split(' ')[0],
             'losses': data[3].split(' ')[0], 'goals': data[4].split(' ')[0]}

    team2 = {'name': data[5], 'wins': data[6].split(' ')[0], 'draws': data[7].split(' ')[0],
             'losses': data[8].split(' ')[0], 'goals': data[9].split(' ')[0]}

    print(team1)
    print(team2)


# this method add more data to the dicts from get_team_stats() method
# call this method from get_team_stats() method to expand the data about the teams in the dicts
def get_team_stats_extra(driver, team1, team2):
    element = driver.find_element(By.ID, 'team_stats_extra')
    data = element.text.split('\n')

    # remove white spaces from left and right
    for i in range(len(data)):
        data[i] = data[i].lstrip()  # remove white spaces from left
        data[i] = data[i].rstrip()  # remove white spaces from right

    team1_name = data[0]
    team2_name = data[1]

    # the names of the teams appears more than once, removing them as long as they're in the list
    # when the elements won't be at the list anymore, exception will be thrown (remove method remove only one element)
    try:
        while True:
            data.remove(team1['name'])
            data.remove(team2['name'])
    except:
        pass

    # create dictionaries with the extra data
    team1_extra = {'name': team1_name, 'fouls': data[0], 'corners': data[3], 'crosses': data[6], 'touches': data[9],
                   'tackles': data[12], 'interceptions': data[15], 'aerials won': data[18], 'clearances': data[21],
                   'offsides': data[24], 'goal kicks': data[27], 'throw ins': data[30], 'long balls': data[33]}

    team2_extra = {'name': team2_name, 'fouls': data[2], 'corners': data[5], 'crosses': data[8], 'touches': data[11],
                   'tackles': data[14], 'interceptions': data[17], 'aerials won': data[20], 'clearances': data[23],
                   'offsides': data[26], 'goal kicks': data[29], 'throw ins': data[32], 'long balls': data[35]}

    # update the teams dictionaries with the extra data dictionaries
    team1.update(team1_extra)
    team2.update(team2_extra)


# this method will get the team stats from the game, to get extra stats, call get_team_stats_extra()
# function and pass team1 and team2 dicts as arguments
def get_team_stats(driver):
    element = driver.find_element(By.ID, 'team_stats')
    data = element.text.split('\n')
    # init dict for teams
    team1 = {'possession': data[3], 'successful passes': data[6].split(' ')[0],
             'total pass attempts': data[6].split(' ')[2], 'pass accuracy': data[6].split(' ')[-1],
             'shots on target': data[9].split(' ')[0], 'shots': data[9].split(' ')[2],
             'shots accuracy': data[9].split(' ')[-1], 'shots on goal': data[12].split(' ')[2],
             'saves': data[12].split(' ')[0]}
    team2 = {'possession': data[4], 'successful passes': data[7].split(' ')[2],
             'total pass attempts': data[7].split(' ')[-1], 'pass accuracy': data[7].split(' ')[0],
             'shots on target': data[10].split(' ')[2], 'shots': data[10].split(' ')[-1],
             'shots accuracy': data[10].split(' ')[0], 'shots on goal': data[13].split(' ')[-1],
             'saves': data[13].split(' ')[2]}  # init dict for team2
    # yellow cards parameter are not textual, pulling the yellow cards elements array to calc the number
    cards_elements = driver.find_elements(By.CLASS_NAME, 'cards')
    team1['yellow cards'] = str(len(cards_elements[0].find_elements(By.CLASS_NAME, 'yellow_card')))
    team2['yellow cards'] = str(len(cards_elements[1].find_elements(By.CLASS_NAME, 'yellow_card')))
    get_team_stats_extra(driver, team1, team2)
    return team1, team2


# this method pulls the team stats data and writes it to csv
def team_stats_to_csv(driver, file_path):
    team1, team2 = get_team_stats(driver)  # get the teams dictionaries with the relevant data
    f = open(file_path, 'a', encoding='utf-8')  # open file with append
    f.write('match stats\n')  # table headline
    headline = team1.keys()  # dictionary key set contains the table features
    headline = ','.join(headline)  # concat the features with , to get csv
    team1_stats = team1.values()  # get values of team1
    team1_stats = ','.join(team1_stats)  # concat the values with , for csv
    # same for team2
    team2_stats = team2.values()
    team2_stats = ','.join(team2_stats)
    # write the data to the csv file
    f.write(f'{headline}\n')
    f.write(f'{team1_stats}\n')
    f.write(f'{team2_stats}\n')


def get_head_to_head_last5(driver):
    element = driver.find_element(By.ID, 'games_history_all')  # find game history table
    match_count = 0  # count the games, we need only 5 of them
    match_reports = []
    rows = element.find_elements(By.TAG_NAME, 'tr')  # get the table's rows
    for row in rows:
        tds = row.find_elements(By.CLASS_NAME, 'left')  # get the columns that may be the match report column
        for td in tds:
            if td.get_attribute('data-stat') == 'match_report':  # make sure we're at the right column
                a_tag = td.find_elements(By.TAG_NAME, 'a')  # get the 'a' tag from the column tag
                if len(a_tag) == 1:  # make sure there is a match report (sometimes there are future games in table)
                    match_reports.append(a_tag.__getitem__(0).get_attribute('href'))  # insert the link to the list
                    match_count += 1  # update the match count
                    # finish after 5 matches
                    if match_count == 5:
                        return match_reports
