from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	"""自定义用户"""
	alias = models.CharField(max_length=20, default='', verbose_name='别名')
	department=models.CharField(max_length=20, default='', verbose_name='部门')
	class Meta(AbstractUser.Meta):
		pass
