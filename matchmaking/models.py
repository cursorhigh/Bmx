from django.db import models
from django.utils import timezone
class matchmaking(models.Model):
    player_id = models.CharField(max_length=255, primary_key=True)
    category = models.CharField(max_length=255)
