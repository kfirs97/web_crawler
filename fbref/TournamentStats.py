from selenium.webdriver.common.by import By
import fbref.TeamStats as TeamStats
import fbref.PlayerStats as PlayerStats


def get_match_info(driver):
    element = driver.find_element(By.CLASS_NAME, 'scorebox')
    data = element.text.split('\n')
    match_info = {'date': data[14].split('(')[0].rstrip(), 'attendance': data[18].split(': ')[1],
                  'Venue': data[19].split(': ')[1].replace(',', '')}
    return match_info


# this method using team_stats_to_csv() and player_stats_to_csv() to write a full match report to csv
def entire_match_report_to_csv(driver, file_path):
    f = open(file_path, 'w', encoding='utf-8')  # open the file for writing
    TeamStats.team_stats_to_csv(driver, file_path)  # call the method with the file path
    PlayerStats.player_stats_to_csv(driver, file_path)  # call the method with te file path
    f.close()  # close the file


def entire_season_to_csv(driver):
    links_list = []
    # Find all elements with the tag "a" and the text "Match Report"
    elements = driver.find_elements(By.XPATH, "//a[text()='Match Report']")
    for element in elements:
        links_list.append(element.get_attribute("href"))  # collect all the match_report links to list

    i = 1
    for link in links_list:
        driver.get(link)  # get the current match report link
        entire_match_report_to_csv(driver,f'match_{i}.csv')  # save the match report to csv
        i += 1
