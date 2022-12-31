# web_crawler
get data from sports statistics sites

This repository pulls football statistics data from different sites, each site have is own package.
In any site package we have 3 diffrernt modules, PlayerStats, TeamStats, TournamentStats

## PlayerStats
In each match report at fbref there's also a table for the teams players stats, this module will pull this data 
### functoins
- get_match_player stats() 
  get the player stats table data and store it in a python list
- player_stats_to_csv(file_path)
  pull the player stats table data and store in in a csv file at the given file path

*when calling this function, make sure your driver is in a match report page

