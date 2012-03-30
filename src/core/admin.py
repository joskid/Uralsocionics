# -*- coding: utf-8 -*-
from django.contrib import admin
from src.core.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'nick', 'phone', 'birthdate')


class IllustrationInline(admin.StackedInline):
    model = Illustration
    extra = 3


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'slug', 'date_created')
    filter_horizontal = ('authors', 'category')
    inlines = [IllustrationInline]
    ordering = ['-date_created']


class IllustrationAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_title', 'image')


class EventDayAdmin(admin.ModelAdmin):
    list_display = ('date',)
    ordering = ['-date']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Edition)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Illustration, IllustrationAdmin)
admin.site.register(EventDay, EventDayAdmin)
admin.site.register(Comment)
