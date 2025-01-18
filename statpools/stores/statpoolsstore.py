import datetime

from statpools.services.nflapiservice import NFLApiService
from statpools.constants import NFLTeamConstants
from statpools import models

class StatPoolsStore():
    def GetCurrentWeekGames():
        #Get Current Week???
        games = NFLApiService.GetUpcomingNFLGames()
        result = []
        for idx, game in games.iterrows():
            id_split = game['game_id'].split('_')
            game_id = str(game['espn'])+'_'+id_split[1]+'_'+id_split[2]+'_'+id_split[3]
            result.append({'id':game_id, 'date':game['gameday'],
                           'home':NFLTeamConstants.NAME[game['home_team']], 'away':NFLTeamConstants.NAME[game['away_team']],
                           'hlogo':NFLTeamConstants.LOGO[NFLTeamConstants.NAME[game['home_team']]],
                           'alogo':NFLTeamConstants.LOGO[NFLTeamConstants.NAME[game['away_team']]] })
        return result
            
    def GetGamePlayers(gameid):
        gameIdSplit = gameid.split("_")
        players = NFLApiService.GetWeeklyRosters(gameIdSplit[1], [gameIdSplit[3], gameIdSplit[2]])
        players = players[players['position'].isin(['QB','RB','WR','TE','K'])]
        result = []
        for idx, player in players.iterrows():
            result.append({'id':player['espn_id'], 'num':int(player['jersey_number']), 
                           'pos':player['position'],
                           'name':player['player_name'], 'img':player['headshot_url']})
        return result
    
    def GetStatOptions(pos):
        result = []
        for stat in NFLTeamConstants.STATS:
            if pos in stat['positions']:
                result.append(stat)
        return result

    def GetStatByKey(statKey):
        for stat in NFLTeamConstants.STATS:
            if stat['key'] == statKey:
                return stat
        raise Exception("Stat not Found")        

    def GetCategoriesData(categories, statpooluser):
        result = []
        for cat in categories:
            player = NFLApiService.GetPlayerInfo(cat.player_id)
            teamName = player['team']['$ref'].split('/')[-1]
            teamName = teamName[0:teamName.index('?')]
            userpick = models.StatPoolUserPick.objects.filter(stat_pool_user=statpooluser, stat_pool_category=cat).first()
            date_now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5)
            result.append({
                'id':cat.id,
                'value':cat.value,
                'player':{
                    'id':cat.player_id,
                    'name':player['displayName'],
                    'num':player['jersey'],
                    'pos':player['position']['abbreviation'],
                    'team': NFLTeamConstants.ID[teamName],
                    'team_logo':NFLTeamConstants.LOGO[ NFLTeamConstants.ID[teamName] ],
                    'img':player['headshot']['href']
                },
                'game':{
                    'id':cat.game_id,
                    'desc': cat.game_desc,
                    'start_time':cat.game_datetime,
                    'started':(date_now > cat.game_datetime),
                    'status': cat.game_status
                },
                'stat': StatPoolsStore.GetStatByKey(cat.stat_id),
                'userpick': userpick
            })
        return result
    
    def GetStatPoolData(self, user):
        result = []
        users_statpools = models.StatPoolUser.objects.filter(user_id=user)
        for user_statpool in users_statpools:
            statpool = user_statpool.stat_pool_id
            result.append({
                'id':statpool.id,
                'name':statpool.name,
                'owner':statpool.owner.username,
                'user_count': models.StatPoolUser.objects.filter(stat_pool_id=statpool.id).count(),
                'user_status': self.GetUsersStatPoolStatus(statpool, user_statpool)
            })
        return result

    def GetUsersStatPoolStatus(self, statpool, user):
        categories = models.StatPoolCategory.objects.filter(stat_pool=statpool).count()
        picks = models.StatPoolUserPick.objects.filter(stat_pool_user=user).count()
        if picks == 0:
            return "Not Started"
        elif picks == categories:
            return "Picks Complete"
        else:
            return "Picks In Progress"

    def GetUserStats(user):
        stats={}
        stat_pool_users = models.StatPoolUser.objects.filter(user_id=user)
        if (stat_pool_users.count() == 0):
            return {
                'pools_played': 0,
                'wins': 0,
                'best_pool': {'name':'', 'score':'NA'}
            }
        stats['pools_played'] = stat_pool_users.count()
        stat_pools = stat_pool_users.values_list('stat_pool_id', flat=True)
        wins = 0
        for pool in stat_pools:
            winner = models.StatPoolUser.objects.filter(stat_pool_id=pool).order_by('score').first()
            if winner.user_id == user:
                wins+=1
        stats['wins'] = wins
        best_score = stat_pool_users.order_by('score').first()
        stats['best_pool'] = {
            'name':best_score.stat_pool_id.name,
            'score':best_score.score
        }
        return stats
