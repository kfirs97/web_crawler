from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from debug.Debug import Debug


# this method will get the team stats from the game, to get extra stats, call get_team_stats_extra()
# function and pass team1 and team2 dicts as arguments
def get_team_stats():
    element = driver.find_element(By.ID, 'team_stats')
    data = element.text.split('\n')
    team1 = {}  # init dict for team1
    team2 = {}  # init dict for team2

    # split the row data and put at the right keys for each team
    team1['name'] = data[1].split(' ')[0]
    team2['name'] = data[1].split(' ')[1]

    team1['possessiom'] = data[3]
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
    team1['yellow cards'] = len(cards_elements[0].find_elements(By.CLASS_NAME, 'yellow_card'))
    team2['yellow cards'] = len(cards_elements[1].find_elements(By.CLASS_NAME, 'yellow_card'))


# this method add more data to the dicts from get_team_stats() method
# call this method from get_team_stats() method to expand the data about the teams in the dicts
def get_team_stats_extra(team1, team2):
    element = driver.find_element(By.ID, 'team_stats_extra')
    data = element.text.split('\n')

    team1['fouls'] = data[2]
    team2['fouls'] = data[4]

    team1['corners'] = data[5]
    team2['corners'] = data[7]

    team1['crosses'] = data[8]
    team2['crosses'] = data[10]

    team1['touches'] = data[11]
    team2['touches'] = data[13]

    team1['tackles'] = data[16]
    team2['tackles'] = data[18]

    team1['interceptions'] = data[19]
    team2['interceptions'] = data[21]

    team1['aerials won'] = data[22]
    team2['aerials won'] = data[24]

    team1['clearances'] = data[25]
    team2['clearances'] = data[27]

    team1['offsides'] = data[30]
    team2['offsides'] = data[32]

    team1['goal kicks'] = data[33]
    team2['goal kicks'] = data[35]

    team1['throw ins'] = data[36]
    team2['throw ins'] = data[38]

    team1['long balls'] = data[39]
    team2['long balls'] = data[41]


# this method pulls the teams players stats and add the data in list for each team
def get_match_players_stats():
    # pull the elements that represents the players stats tables
    elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')
    data1 = elements[0].text.split('\n')  # team1 data
    data2 = elements[1].text.split('\n')  # team2 data
    team1 = []
    team2 = []

    # add the rows to array of each team, each row represents team players stats
    for i in range(2, len(data1)):
        team1.append(data1[i])
        team2.append([data2[i]])


# this method pulls the teams players stats and writes the data in a csv file
def player_stats_to_csv():
    # pull the elements that represents the players stats tables
    elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')
    data1 = elements[0].text.split('\n')  # team1 data
    data2 = elements[1].text.split('\n')  # team2 data
    table_headline = data1[1].replace(' ', ',')  # save the headline row for the table

    # extract relevant rows data rows
    data1 = data1[2:len(data1)]
    data2 = data2[2:len(data2)]

    f = open('player_stats.csv', 'w', encoding='utf-8')  # open csv file for writing
    f.write('team1\n')  # table1 headline
    f.write(f'{table_headline}\n') # write table parameters
    # find the player name (could be more than 1 word and we split by blanks
    for row in data1:
        index = 0
        while not row[index].isnumeric():
            index += 1

        name = row[0: index]  # extract the player's name
        row_csv = row[index:len(row)]  # extract the rest of data
        row_csv = row_csv.replace(',', '-')  # replace , with - to avoid data leaks to no relevant columns
        row_csv = row_csv.split(' ')  # split the data to array
        row_csv.pop(1)  # pop out the nation's name because it appears twice
        row_csv = ','.join(row_csv)  # contact the strings of the array with , to create csv
        f.write(f'{name},{row_csv}\n')  # write the name and the data to the csv file

    # repeat the process for team2
    f.write('\nteam2\n')
    f.write(f'{table_headline}\n')
    for row in data2:
        index = 0
        while not row[index].isnumeric():
            index += 1

        name = row[0: index]
        row_csv = row[index:len(row)]
        row_csv = row_csv.replace(',', '-')
        row_csv = row_csv.split(' ')
        row_csv.pop(1)
        row_csv = ','.join(row_csv)
        f.write(f'{name},{row_csv}\n')


# elements = driver.find_elements(By.CLASS_NAME, 'hasmore')
# for element in elements:
#     driver.execute_script("arguments[0].setAttribute('class', 'hasmore drophover')", element)
#
#     elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')

PATH = 'C:\kfir\Projects\chrome_webdriver\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://fbref.com/en/matches/15996455/Dortmund-Barcelona-September-17-2019-Champions-League')
driver.implicitly_wait(2)
# elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')
# for element in elements:
#     print(element.text)
player_stats_to_csv()
