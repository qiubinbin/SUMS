from django.urls import re_path

from part02 import views

urlpatterns = [
	re_path('submit_comment', views.submit_comment, name='submit_comment'),
]
