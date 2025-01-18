from statpools.services.nflapiservice import NFLApiService
from statpools.constants import NFLTeamConstants, StatPoolConstants
from statpools import models
import datetime

class ScoringStore():
    def ScoreGames(self):
        today = datetime.datetime.now() - datetime.timedelta(hours=5)
        categories = models.StatPoolCategory.objects.filter(game_datetime__lt=today).exclude(game_status="STATUS_SCORED")
        for category in categories:
            gameStats = NFLApiService.GetPlayerStats(category.game_id, category.player_id)
            gameStatus = NFLApiService.GetGameStatus(category.game_id)
            stat = self.GetStatByKey(category.stat_id)
            value = [p_stat for p_stat in gameStats[stat['idx']]['stats'] if p_stat['name'] == stat['key']]
            if len(value) == 1:
                print("Scoring category "+ str(category.id) + " ("+category.game_desc+")")
                category.value = value[0]['value']
                category.game_status = gameStatus['type']['detail']
                category.save()
                if gameStatus['type']['name'] == "STATUS_FINAL":
                    self.ScoreUserPicks(category)
                    category.game_status = "STATUS_SCORED"
                    category.save()
                    print("Category " + str(category.id) + " ("+category.game_desc+") has finished scoring.")
            else:
                print("ERROR - Category " + str(category.id) + " ("+category.game_desc+") gave 2 values.")
        return

    def ScoreUserPicks(self, category):
        stat_pool_users = models.StatPoolUser.objects.filter(stat_pool_id=category.stat_pool)
        userPicks = models.StatPoolUserPick.objects.filter(stat_pool_category=category)
        for user in stat_pool_users:
            pick = userPicks.filter(stat_pool_user=user).first()
            score = category.value
            if pick:
                score = float(abs(pick.value - float(category.value)))
            user.score += score
            user.save()
            print("\tUser Pick for category " + str(category.id) + " ("+category.game_desc+") has been scored.")
        return

    def GetStatByKey(self, statKey):
        for stat in NFLTeamConstants.STATS:
            if stat['key'] == statKey:
                return stat
        raise Exception("Stat not Found")
    
    def UpdateStatPoolsStatus(self):
        stat_pools = models.StatPool.objects.exclude(status="Complete")
        for pool in stat_pools:
            categories = models.StatPoolCategory.objects.filter(stat_pool=pool).exclude(game_status="STATUS_SCORED")
            if categories.count() == 0:
                pool.status = "Complete"
                pool.save()
                print("\tStat Pool " + str(pool.name)+ " is complete.")
        return