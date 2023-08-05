from django.db import models
class matchmaking(models.Model):
    player_id = models.CharField(max_length=255, primary_key=True)
    playername = models.CharField(max_length=255,default='none')
    category = models.CharField(max_length=255)