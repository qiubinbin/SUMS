from django.contrib import admin

from .models import Comment


# Register your models here.
@admin.register(Comment)
class NoteAdmin(admin.ModelAdmin):
	list_display = ('id','content_object', 'content', 'comment_time', 'user',)
