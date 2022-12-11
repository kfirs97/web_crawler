from selenium.webdriver.common.by import By
from fbref.TeamStats import TeamStats
from fbref.PlayerStats import PlayerStats


class TournamentStats:
    @staticmethod
    # this method using team_stats_to_csv() and player_stats_to_csv() to write a full match report to csv
    def entire_match_report_to_csv(driver):
        file_name = 'match_report.csv'  # open the file for writing
        f = open(file_name, 'w', encoding='utf-8')
        TeamStats.team_stats_to_csv(driver, file_name)  # call the method with the file path
        PlayerStats.player_stats_to_csv(driver, file_name)  # call the method with te file path
        f.close()  # close the file

    @staticmethod
    def entire_season(driver):
        links_list = []
        # Find all elements with the tag "a" and the text "Match Report"
        elements = driver.find_elements(By.XPATH, "//a[text()='Match Report']")
        for element in elements:
            links_list.append(element.get_attribute("href"))  # collect all the match_report links to list

        for link in links_list:
            driver.get(link)  # get the current match report link
            TournamentStats.entire_match_report_to_csv(driver)  # save the match report to csv
