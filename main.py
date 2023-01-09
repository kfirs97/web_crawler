from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from debug.Debug import Debug
from fbref import TournamentStats
from fbref import TeamStats
from fbref import PlayerStats

# relevant test links
ARSENAL_VS_PALACE = 'https://fbref.com/en/matches/e62f6e78/Crystal-Palace-Arsenal-August-5-2022-Premier-League'
HEAD_TO_HEAD = 'https://fbref.com/en/stathead/matchup/teams/47c64c55/18bb7c10/Crystal-Palace-vs-Arsenal-History#coverage'
BARCELONA_VS_DORTMUND = 'https://fbref.com/en/matches/15996455/Dortmund-Barcelona-September-17-2019-Champions-League'
PL = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'

# paths for web driver
KFIR_WINDOWS_PATH = 'C:\kfir\Projects\chrome_webdriver\chromedriver.exe'
KFIR_UBUNTU_PATH = '/usr/bin/chromedriver'

driver = webdriver.Chrome(KFIR_UBUNTU_PATH)  # initialize driver
driver.get(PL)  # go to the starting page
driver.implicitly_wait(2)  # wait
# write code here
TournamentStats.entire_season_to_csv(driver)
driver.close()