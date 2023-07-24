from django.contrib import admin
from .models import User, UserSKills

admin.site.register([
    User
])

admin.site.register([
    UserSKills
])
