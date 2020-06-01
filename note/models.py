# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from django.db import models


class Section(models.Model):
	section = models.CharField(max_length=10)  # 部门

	class Meta:
		verbose_name = '部门'
		verbose_name_plural = '部门'

	def __str__(self):
		return self.section


class Principal(models.Model):
	name = models.CharField(max_length=128, unique=True)  # 用户名唯一
	password = models.CharField(max_length=16)
	c_time = models.DateTimeField(auto_now_add=True)
	section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['c_time']
		verbose_name = '负责人'
		verbose_name_plural = '负责人'


class UserForm(forms.Form):
	username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}),
	                           required=True)
	password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
	                           required=True)


class Note(models.Model):
	"""一则升级记录"""
	title = models.CharField(max_length=50)  # 升级名称
	time = models.DateField(auto_now=False)  # 升级时间
	content = RichTextUploadingField()  # 主要内容
	author = models.ForeignKey(Principal, on_delete=models.DO_NOTHING)  # 负责人
	annex = models.FileField(upload_to="static/files/")  # 附件

	def __str__(self):
		return "<软件升级：%s>" % self.title

	class Meta:
		verbose_name = '升级'
		verbose_name_plural = '升级'
		ordering = ['-time']
