from django.contrib import admin

from news.models import News, Hashtag


admin.site.register(News)
admin.site.register(Hashtag)
