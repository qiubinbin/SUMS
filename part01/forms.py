from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',
	                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
	password = forms.CharField(label='密码',
	                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

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
	username = forms.CharField(label='用户名', max_length=30, min_length=3,
	                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
	email = forms.EmailField(label='邮箱',
	                         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输如邮箱地址'}))
	password = forms.CharField(label='密码', min_length=6,
	                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
	password_again = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
