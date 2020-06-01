from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()  # 非外键


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

	def clean(self):
		"""数据验证"""
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("用户名或密码不正确！")
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data


class RegForm(forms.Form):
	username = forms.CharField(max_length=30, min_length=3,
	                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名!'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输如邮箱地址!'}))
	password = forms.CharField(min_length=6,
	                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码!'}))
	password_again = forms.CharField(min_length=6, widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': '请再次输入密码!'}))

	"""验证需clean_开头:django的forms.py的运行顺序，
	是先执行定义字段的语句，然后查找是否有定义该字段对应
	的clean_xxx函数，如果有，则执行该函数"""

	def clean_username(self):
		"""验证用户名"""
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已存在!')
		return username

	def clean_email(self):
		"""验证邮箱"""
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已存在!')
		return email

	def clean_password_again(self):
		"""验证密码一致"""
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('两次密码不一致!')
		return password_again

class ChangAlias(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))