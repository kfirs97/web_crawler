from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from debug.Debug import Debug
from fbref.TournamentStats import TournamentStats
import numpy as np


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

    get_team_stats_extra(team1, team2)
    return team1, team2


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

    team1['tackles'] = data[14]
    team2['tackles'] = data[16]

    team1['interceptions'] = data[17]
    team2['interceptions'] = data[19]

    team1['aerials won'] = data[20]
    team2['aerials won'] = data[22]

    team1['clearances'] = data[23]
    team2['clearances'] = data[25]

    team1['offsides'] = data[26]
    team2['offsides'] = data[28]

    team1['goal kicks'] = data[29]
    team2['goal kicks'] = data[31]

    team1['throw ins'] = data[32]
    team2['throw ins'] = data[34]

    team1['long balls'] = data[35]
    team2['long balls'] = data[37]


# this method pulls the team stats data and writes it to csv
def team_stats_to_csv(file_path):
    team1, team2 = get_team_stats()  # get the teams dictionaries with the relevant data
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
def player_stats_to_csv(file_path):
    # pull the elements that represents the players stats tables
    elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')
    data1 = elements[0].text.split('\n')  # team1 data
    data2 = elements[1].text.split('\n')  # team2 data
    table_headline = data1[1].replace(' ', ',')  # save the headline row for the table

    # extract relevant rows data rows
    data1 = data1[2:len(data1)]
    data2 = data2[2:len(data2)]

    f = open(file_path, 'a', encoding='utf-8')  # open csv file for writing
    f.write('\nteam1\n')  # table1 headline
    f.write(f'{table_headline}\n')  # write table parameters
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


# this method using team_stats_to_csv() and player_stats_to_csv() to write a full match report to csv
def entire_match_report_to_csv():
    file_name = 'match_report.csv'  # open the file for writing
    f = open(file_name, 'w', encoding='utf-8')
    team_stats_to_csv(file_name)  # call the method with the file path
    player_stats_to_csv(file_name)  # call the method with te file path
    f.close()  # close the file


def entire_season():
    links_list = []
    # Find all elements with the tag "a" and the text "Match Report"
    elements = driver.find_elements(By.XPATH, "//a[text()='Match Report']")
    for element in elements:
        links_list.append(element.get_attribute("href"))  # collect all the match_report links to list

    for link in links_list:
        driver.get(link)  # get the current match report link
        entire_match_report_to_csv()  # save the match report to csv


ARSENAL_VS_PALACE = 'https://fbref.com/en/matches/e62f6e78/Crystal-Palace-Arsenal-August-5-2022-Premier-League'
BARCELONA_VS_DORTMUND = 'https://fbref.com/en/matches/15996455/Dortmund-Barcelona-September-17-2019-Champions-League'

KFIR_WINDOWS_PATH = 'C:\kfir\Projects\chrome_webdriver\chromedriver.exe'
KFIR_UBUNTU_PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(KFIR_WINDOWS_PATH)
driver.get(ARSENAL_VS_PALACE)
driver.implicitly_wait(2)
# elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')d
# for element in elements:
#     print(element.text)
#entire_match_report_to_csv()
TournamentStats.entire_match_report_to_csv(driver)
driver.close()

