from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from part02.forms import CommentForm
from part02.models import Comment
from . import models
from .forms import LoginForm, RegForm


# Create your views here.

def home(request):
	return render(request, 'home.html')


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
	return render(request, 'login.html', context)


def login4ui(request):
	"""界面登录"""
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(request, username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return render(request, 'home.html')
	else:
		return render(request, 'login.html', {'message': "用户名或密码不正确！"})


def logout(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(request, username=username, password=password)
	if user is not None and user.is_active:
		auth.logout(request, user)
		return render(request, 'login.html')
	else:
		pass


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


def note_list(request):
	notes_all_list = models.Note.objects.all()
	paginator = Paginator(notes_all_list, settings.EACH_PAGE_NOTES_NUMBER)
	page_num = request.GET.get('page', 1)  # 获取页面参数
	page_of_notes = paginator.get_page(page_num)
	current_page_num = page_of_notes.number  # 当前页码
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))  # 页码范围
	if page_range[0] - 1 >= 2:  # 加省略
		page_range.insert(0, '···')
	if page_range[0] != 1:  # 加首页
		page_range.insert(0, 1)
	if paginator.num_pages - page_range[-1] >= 2:  # 加省略
		page_range.append('···')
	if page_range[-1] != paginator.num_pages:  # 加尾页
		page_range.append(paginator.num_pages)
	context = {}
	context['note_dates'] = models.Note.objects.dates('time', 'month', order='DESC')
	context['page_range'] = page_range
	context['page_of_notes'] = page_of_notes
	context['note_sections'] = models.Section.objects.all()
	return render(request, 'note_list.html', context)


def note_detail(request, note_id):
	context = {}
	note = get_object_or_404(models.Note, id=note_id)
	note_content_type = ContentType.objects.get_for_model(note)
	comments = Comment.objects.filter(content_type=note_content_type, object_id=note.pk)
	context['note'] = note
	context['previous_note'] = models.Note.objects.filter(time__gt=note.time).last()  # 前一条
	context['next_note'] = models.Note.objects.filter(time__lt=note.time).first()  # 后一条
	context['note_sections'] = models.Section.objects.all()
	context['note_dates'] = models.Note.objects.dates('time', 'month', order='DESC')
	context['comments'] = comments
	context['comment_form'] = CommentForm(initial={'content_type': note_content_type.model, 'object_id': note_id})
	return render(request, 'note_detail.html', context)


def notes_with_section(request, section_id):
	context = {}
	note_section = get_object_or_404(models.Section, pk=section_id)
	# note_author=get_object_or_404(User,section_id)
	notes_all_list = models.Note.objects.filter(author__section=note_section)  # 获取当前section下所有的note
	paginator = Paginator(notes_all_list, settings.EACH_PAGE_NOTES_NUMBER)
	page_num = request.GET.get('page', 1)  # 获取页面参数
	page_of_notes = paginator.get_page(page_num)
	current_page_num = page_of_notes.number  # 当前页码
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))  # 页码范围
	if page_range[0] - 1 >= 2:  # 加省略
		page_range.insert(0, '···')
	if page_range[0] != 1:  # 加首页
		page_range.insert(0, 1)
	if paginator.num_pages - page_range[-1] >= 2:  # 加省略
		page_range.append('···')
	if page_range[-1] != paginator.num_pages:  # 加尾页
		page_range.append(paginator.num_pages)
	context['notes'] = notes_all_list
	context['page_range'] = page_range
	context['page_of_notes'] = page_of_notes
	context['note_section'] = note_section
	context['note_sections'] = models.Section.objects.all()
	context['note_dates'] = models.Note.objects.dates('time', 'month', order='DESC')
	return render(request, 'notes_with_section.html', context)


def notes_with_date(request, year, month):
	context = {}
	print(year, month)
	notes_all_list = models.Note.objects.filter(time__year=year, time__month=month)  # 查询某一月全部博客
	print(notes_all_list)
	paginator = Paginator(notes_all_list, settings.EACH_PAGE_NOTES_NUMBER)
	page_num = request.GET.get('page', 1)  # 获取页面参数
	page_of_notes = paginator.get_page(page_num)
	current_page_num = page_of_notes.number  # 当前页码
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))  # 页码范围
	if page_range[0] - 1 >= 2:  # 加省略
		page_range.insert(0, '···')
	if page_range[0] != 1:  # 加首页
		page_range.insert(0, 1)
	if paginator.num_pages - page_range[-1] >= 2:  # 加省略
		page_range.append('···')
	if page_range[-1] != paginator.num_pages:  # 加尾页
		page_range.append(paginator.num_pages)
	context['note_dates'] = models.Note.objects.dates('time', 'month', order='DESC')
	context['notes'] = notes_all_list
	context['page_range'] = page_range
	context['page_of_notes'] = page_of_notes
	context['note_sections'] = models.Section.objects.all()
	context['note_date'] = '%s年%s月' % (year, month)
	return render(request, 'notes_with_date.html', context)


def new_note(request):
	print('kaishi')
	new_title = request.POST.get('iname')
	new_time = request.POST.get('itime')
	new_content = request.POST.get('icontent', '')
	new_author = get_object_or_404(models.User, name=request.user)
	new_annex = request.POST.get('iannex')
	new_note = models.Note(title=new_title, time=new_time, content=new_content, author=new_author, annex=new_annex)
	new_note.save()
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	return redirect(referer)
