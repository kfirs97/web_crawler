from selenium.webdriver.common.by import By


# this method add more data to the dicts from get_team_stats() method
# call this method from get_team_stats() method to expand the data about the teams in the dicts
def get_team_stats_extra(driver, team1, team2):
    element = driver.find_element(By.ID, 'team_stats_extra')
    data = element.text.split('\n')

    # remove white spaces from left and right
    for i in range(len(data)):
        data[i] = data[i].lstrip()  # remove white spaces from left
        data[i] = data[i].rstrip()  # remove white spaces from right

    team1['name'] = data[0]
    team2['name'] = data[1]

    # the names of the teams appears more than once, removing them as long as they're in the list
    # when the elements won't be at the list anymore, exception will be thrown (remove method remove only one element)
    try:
        while True:
            data.remove(team1['name'])
            data.remove(team2['name'])
    except:
        pass

    print(data)

    team1['fouls'] = data[0]
    team2['fouls'] = data[2]

    team1['corners'] = data[3]
    team2['corners'] = data[5]

    team1['crosses'] = data[6]
    team2['crosses'] = data[8]

    team1['touches'] = data[9]
    team2['touches'] = data[11]

    team1['tackles'] = data[12]
    team2['tackles'] = data[14]

    team1['interceptions'] = data[15]
    team2['interceptions'] = data[17]

    team1['aerials won'] = data[18]
    team2['aerials won'] = data[20]

    team1['clearances'] = data[21]
    team2['clearances'] = data[23]

    team1['offsides'] = data[24]
    team2['offsides'] = data[26]

    team1['goal kicks'] = data[27]
    team2['goal kicks'] = data[29]

    team1['throw ins'] = data[30]
    team2['throw ins'] = data[32]

    team1['long balls'] = data[33]
    team2['long balls'] = data[35]


class TeamStats:
    @staticmethod
    # this method will get the team stats from the game, to get extra stats, call get_team_stats_extra()
    # function and pass team1 and team2 dicts as arguments
    def get_team_stats(driver):
        element = driver.find_element(By.ID, 'team_stats')
        data = element.text.split('\n')
        team1 = {}  # init dict for team1
        team2 = {}  # init dict for team2

        # split the row data and put at the right keys for each team
        # team1['name'] = data[1].split(' ')[0]
        # team2['name'] = data[1].split(' ')[1]

        team1['possession'] = data[3]
        team2['possession'] = data[4]

        team1['successful passes'] = data[6].split(' ')[0]
        team1['total pass attempts'] = data[6].split(' ')[2]
        team1['pass accuracy'] = data[6].split(' ')[-1]

        team2['successful passes'] = data[7].split(' ')[2]
        team2['total pass attempts'] = data[7].split(' ')[-1]
        team2['pass accuracy'] = data[7].split(' ')[0]

        team1['shots on target'] = data[9].split(' ')[0]
        team1['shots'] = data[9].split(' ')[2]
        team1['shots accuracy'] = data[9].split(' ')[-1]

        team2['shots on target'] = data[10].split(' ')[2]
        team2['shots'] = data[10].split(' ')[-1]
        team2['shots accuracy'] = data[10].split(' ')[0]

        team1['shots on goal'] = data[12].split(' ')[2]
        team1['saves'] = data[12].split(' ')[0]

        team2['shots on goal'] = data[13].split(' ')[-1]
        team2['saves'] = data[13].split(' ')[2]

        # yellow cards parameter are not textual, pulling the yellow cards elements array to calc the number
        cards_elements = driver.find_elements(By.CLASS_NAME, 'cards')
        team1['yellow cards'] = str(len(cards_elements[0].find_elements(By.CLASS_NAME, 'yellow_card')))
        team2['yellow cards'] = str(len(cards_elements[1].find_elements(By.CLASS_NAME, 'yellow_card')))

        get_team_stats_extra(driver, team1, team2)
        return team1, team2

    @staticmethod
    # this method pulls the team stats data and writes it to csv
    def team_stats_to_csv(driver, file_path):
        team1, team2 = TeamStats.get_team_stats(driver)  # get the teams dictionaries with the relevant data
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
