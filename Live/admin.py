from django.contrib import admin

from .models import Match, Over, Batting, Extra,CustomUser


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Match)
admin.site.register(Over)       
admin.site.register(Batting)  
admin.site.register(Extra)