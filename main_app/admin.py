from django.contrib import admin
from .models import Game, Playing, Platform, Photo

# Register your models here.
admin.site.register(Game)
admin.site.register(Playing)
admin.site.register(Platform)
admin.site.register(Photo)