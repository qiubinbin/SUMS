# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.Principal)
class NoteTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'section', 'c_time')


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'section')


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
	list_display = ('title', 'time', 'content', 'author', 'annex',)
