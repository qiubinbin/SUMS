# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models


class Section(models.Model):
	section = models.CharField(max_length=10)  # 部门

	class Meta:
		verbose_name = '部门'
		verbose_name_plural = '部门'

	def __str__(self):
		return self.section


class Note(models.Model):
	"""一则升级记录"""
	title = models.CharField(max_length=50)  # 升级名称
	time = models.DateField(auto_now=False)  # 升级时间
	content = RichTextUploadingField()  # 主要内容
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)  # 负责人
	annex = models.FileField(upload_to="static/files/")  # 附件
	version = models.CharField(max_length=50)  # 当前版本
	section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)

	def __str__(self):
		return "<软件升级：%s>" % self.title

	class Meta:
		verbose_name = '升级'
		verbose_name_plural = '升级'
		ordering = ['-time']
