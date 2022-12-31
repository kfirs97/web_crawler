# web_crawler
get data from sports statistics sites

This repository pulls football statistics data from different sites, each site have is own package.
In any site package we have 3 diffrernt modules, PlayerStats, TeamStats, TournamentStats

## PlayerStats
In each match report at fbref there's also a table for the teams players stats from the game, this module will pull this data 
### Functoins
- get_match_player stats() \
  Get the player stats table data and store it in a python list
- player_stats_to_csv(file_path) \
  Pull the player stats table data and store in in a csv file at the given file path

*** When calling this functions, make sure your driver is in a match report page

## TeamStats
This module will retreive from the site data about the teams
### Functions
#### match report functions
- get_team_stats() \
  Pulls the team stats from the match report page and store it in a dictionary for each team when the key is the name of attribute
- get_team_stats_extra() \
  Helper function for get_team_stats() function, pulls deeper data from the match report, get_team_stats() will use this method to get all of the teams data from the       match report
- team_stats_to_csv(file_path) \
  pulls the team stats data and store it in a csv file at the given file path

*** When calling this functions, make sure your driver is in a match report page

#### head to head functions
- get_head_to_head() \
  Get general data about the last head to head games between the 2 teams (wins, loses, golas, etc) and store it in a dictionary for each team when the key is the         attribute name
- get_head_to_head_last5() \
  Provide a list with links for the match reports of the last match ups between the teams
  
* When calling this function, make sure your driver is in a head to head page

## TournamentStats
This module will pull relevant data about the tournament that both teams competing at
### Functions
- get_match_info() \
  Retreive general info about the game settings (date, attendence, venue, etc)
- entire_match-report_to_csv() \
  Get the whole match report data and store it in a csv file that will contain 3 tables, a table with the teams stats and two more tables for each team's players stats
- entire_season_to_csv() \
  Get the whole season/tournament games match reports and store them in a csv file for each match report in a given folder path. \
  When calling this function, make sure your driver is in a scores & fixtures page of the relevant tournament

  
