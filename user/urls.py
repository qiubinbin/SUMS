from django.urls import re_path

from user import views

urlpatterns = [
	re_path('login/', views.login, name='login'),
	re_path('logout/', views.logout, name='logout'),
	re_path('register/', views.register, name='register'),
	re_path('user_info/', views.user_info, name='user_info'),
	re_path('change_alias/', views.change_alias, name='change_alias'),
	re_path('change_email/', views.change_email, name='change_email'),
]
