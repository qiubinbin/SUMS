from django.urls import re_path

from part01 import views

urlpatterns = [
	re_path('home/', views.home, name='home'),
	re_path('login/', views.login, name='login'),
	re_path('login4ui/', views.login4ui, name='login4ui'),
	re_path('logout/',views.logout,name='logout'),
	re_path('note_list/', views.note_list, name='note_list'),
	re_path('index=(?P<note_id>\d+)', views.note_detail, name='note_detail'),
	re_path('section=(?P<section_id>\d+)', views.notes_with_section, name="notes_with_section"),
	re_path('time=(?P<year>\d+)/(?P<month>\d+)', views.notes_with_date, name="notes_with_time"),
	re_path('new_note', views.new_note, name='new_note'),
]
