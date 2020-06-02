from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, RegForm, ChangAlias

User = get_user_model()


def login(request):
	context = {}
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		login_form = LoginForm()
	context['login_form'] = login_form
	print(login_form)
	return render(request, 'login.html', context)


# def login4ui(request):
# 	"""界面登录"""
# 	username = request.POST['username']
# 	password = request.POST['password']
# 	user = auth.authenticate(request, username=username, password=password)
# 	if user is not None:
# 		auth.login(request, user)
# 		return render(request, 'home.html')
# 	else:
# 		return render(request, 'login.html', {'message': "用户名或密码不正确！"})


def logout(request):
	"""登出"""
	auth.logout(request)
	return redirect(request.GET.get('from', reverse('home')))


def register(request):
	context = {}
	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']
			# 创建用户
			user = User.objects.create_user(username, email, password)
			user.save()
			# 注册后登录
			user = auth.authenticate(request, username=username, password=password)
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		reg_form = RegForm()
	context['reg_form'] = reg_form
	return render(request, 'register.html', context)


def user_info(request):
	context = {}
	return render(request, 'user_info.html', context)


def change_alias(request):
	redirect_to = request.GET.get('from', reverse('home'))
	if request.method == 'POST':
		form = ChangAlias(request.POST, user=request.user)
		if form.is_valid():
			alias_new = form.cleaned_data['alias_new']
			user, _ = User.objects.get_or_create(username=request.user)
			user.alias = alias_new
			user.save()
			return redirect(redirect_to)
	else:
		form = ChangAlias()
	context = {}
	context['form'] = form
	return render(request, 'change_alias.html', context)
