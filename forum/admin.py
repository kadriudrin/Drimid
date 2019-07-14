from django.contrib import admin
from . import models
#from django.contrib.auth.admin import UserAdmin


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main', {'fields': ['user', 'title', 'content', 'total_votes', 'up_votes']}),
        ('Date', {'fields': ['date'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]

    list_display = ('user', 'title', 'total_votes', 'date')

    list_filter = ['date']

    search_fields = ['user', 'title', 'content']


class PostUpVotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

class PostDownVotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PostUpVotes, PostUpVotesAdmin)
admin.site.register(models.PostDownVotes, PostDownVotesAdmin)
#admin.site.register(models.DrimidUser, UserAdmin)
