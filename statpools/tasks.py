from celery import shared_task
from statpools.stores.scoringstore import ScoringStore

@shared_task
def score_games_task():
    print("Scoring Task Started.")
    ScoringStore().ScoreGames()
    print("Scoring Task Completed.")
    pass

@shared_task
def update_stat_pools_status():
    print("Pool Completing Task Started.")
    ScoringStore().UpdateStatPoolsStatus()
    print("Pool Completing Task Completed.")
    pass