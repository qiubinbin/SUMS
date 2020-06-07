# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'section')


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
	list_display = ('title', 'section', 'version', 'time', 'content', 'author', 'annex',)
