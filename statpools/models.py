from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class StatPool(models.Model):
	#id
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=50, default="In Progress")
	
class StatPoolCategory(models.Model):
	#id
	stat_pool = models.ForeignKey(StatPool, on_delete=models.CASCADE)
	player_id = models.CharField(max_length=255)
	player_ref = models.CharField(max_length=255)
	game_id = models.CharField(max_length=255)
	game_desc = models.CharField(max_length=255, default="")
	game_datetime = models.DateTimeField(null=True, default=datetime.now)
	game_status = models.CharField(max_length=50, default="")
	stat_id = models.CharField(max_length=50)
	value = models.FloatField(default=None, null=True, blank=True)
	
class StatPoolUser(models.Model):
	#id
	stat_pool_id = models.ForeignKey(StatPool, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	score = models.FloatField(default=0.0)
	
class StatPoolUserPick(models.Model):
	#id
	stat_pool_category = models.ForeignKey(StatPoolCategory, on_delete=models.CASCADE)
	stat_pool_user = models.ForeignKey(StatPoolUser, on_delete=models.CASCADE)
	value = models.FloatField(default=0.0)