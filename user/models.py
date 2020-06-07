from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	"""自定义用户"""
	alias = models.CharField(max_length=20, default='', verbose_name='别名')
	c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

	class Meta(AbstractUser.Meta):
		pass
