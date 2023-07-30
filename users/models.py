from django.db import models

class User(models.Model):
    rank = models.IntegerField()
    username = models.CharField(primary_key=True, max_length=255)
    email = models.EmailField(unique=True, null=False)
    wins = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ['rank']
    
