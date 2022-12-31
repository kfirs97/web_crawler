from selenium.webdriver.common.by import By


# this method pulls the teams players stats and add the data in list for each team
def get_match_players_stats(driver):
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
def player_stats_to_csv(driver, file_path):
    # pull the elements that represents the players stats tables
    elements = driver.find_elements(By.XPATH, '//*[contains(@id, "switcher_player_stats_")]')
    data1 = elements[0].text.split('\n')  # team1 data
    data2 = elements[1].text.split('\n')  # team2 data
    table_headline = data1[1].replace(' ', ',')  # save the headline row for the table
    # extract relevant rows data rows
    data1 = data1[2:len(data1)]
    data2 = data2[2:len(data2)]
    # open csv file for writing
    f = open(file_path, 'a', encoding='utf-8')
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
