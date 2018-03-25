from django.contrib import admin
from myblog.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','content','pub_time')
    list_filter = ('pub_time',)

admin.site.register(Article,ArticleAdmin)