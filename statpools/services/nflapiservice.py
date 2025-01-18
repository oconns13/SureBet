from time import strftime, strptime
import requests
import json
import nfl_data_py as nfl
from datetime import datetime, timedelta
import pandas as pd

from statpools.constants import NFLTeamConstants

CURRENT_SEASON = 2024

class NFLApiService():
    #Returns datatable [game_id,week,gameday,weekday,gametime,away_team,home_team]
    #Contains the upcoming week of games for the nfl
    def GetUpcomingNFLGames():
        schedules = nfl.import_schedules(years=[CURRENT_SEASON])
        schedules = schedules.drop(columns=['season', 'game_type', 'home_score', 'away_score',
                                            'location', 'result', 'total', 'overtime', 'old_game_id', 'gsis',
                                            'nfl_detail_id', 'pfr', 'pff', 'ftn', 'away_rest', 'home_rest',
                                            'away_moneyline', 'home_moneyline', 'spread_line', 'away_spread_odds',
                                            'home_spread_odds', 'total_line', 'under_odds', 'over_odds', 'div_game',
                                            'roof', 'surface', 'temp', 'wind', 'away_qb_id', 'home_qb_id',
                                            'away_qb_name', 'home_qb_name', 'away_coach', 'home_coach', 'referee',
                                            'stadium_id', 'stadium'])
        #Remove games that are schedule for before today
        schedules['gameday'] = pd.to_datetime(schedules['gameday'] + ' ' + schedules['gametime'])
        schedules = schedules[schedules['gameday'] >= (datetime.now() - timedelta(hours=5))]
        #Get the current weeks games
        weekNum = schedules['week'].min()
        schedules = schedules[schedules['week'] == weekNum]
        return schedules
    
    #Returns datatable [team, position, jersey_number, status, player_name, player_id, headshot_url, week]
    #Contains the active players from the given teams and week number
    def GetWeeklyRosters(weekNum, teams):
        players = nfl.import_weekly_rosters(years=[CURRENT_SEASON])
        players = players.drop(columns=['season', 'depth_chart_position', 'birth_date', 'first_name', 'last_name',
                                        'height', 'weight', 'college', 'years_exp', 'ngs_position', 'game_type', 'esb_id',
                                        'gsis_it_id', 'smart_id', 'entry_year', 'rookie_year', 'draft_club',
                                        'draft_number', 'age', 'football_name', 'status_description_abbr',
                                        'sportradar_id','yahoo_id', 'rotowire_id', 'pff_id', 'pfr_id', 'fantasy_data_id', 
                                        'sleeper_id'])
        players = players[players['week'] == players['week'].max()]
        players = players[players['team'].isin(teams)]
        players = players[players['status'] == 'ACT']
        return players
    
    def GetPlayerInfo(player_id):
        data = requests.get('http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/'+str(CURRENT_SEASON)+'/athletes/'+player_id+'?lang=en&region=us')
        return json.loads( data.text )

    def GetPlayerStats(gameId, playerId):
        gameIdSplit = gameId.split("_")
        teamName = NFLTeamConstants.NAME[gameIdSplit[2]]
        teamId = 0
        for item in NFLTeamConstants.ID:
            if NFLTeamConstants.ID[str(item)] == teamName:
                teamId = item
        response = requests.get("http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/"+str(int(gameIdSplit[0]))+"/competitions/"+str(int(gameIdSplit[0]))+"/competitors/"+str(teamId)+"/roster/"+str(playerId)+"/statistics/0")
        data = json.loads(response.text)
        return data['splits']['categories']
    
    def GetGameStatus(game_id):
        gameIdSplit = game_id.split("_")
        response = requests.get("http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/"+gameIdSplit[0]+"/competitions/"+gameIdSplit[0]+"/status")
        return json.loads(response.text)