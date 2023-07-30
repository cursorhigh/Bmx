from django.contrib import admin
from matchmaking.models import matchmaking
# Register your models here.
from users.models import User
admin.site.register(User)
admin.site.register(matchmaking)