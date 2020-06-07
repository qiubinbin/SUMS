from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from flow.forms import CommentForm
from flow.models import Comment
from . import models

User = get_user_model()


# Create your views here.

def home(request):
	return render(request, 'home.html')


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
	comments = Comment.objects.filter(content_type=note_content_type, object_id=note.pk, parent=None)
	context['note'] = note
	context['previous_note'] = models.Note.objects.filter(time__gt=note.time).last()  # 前一条
	context['next_note'] = models.Note.objects.filter(time__lt=note.time).first()  # 后一条
	context['note_sections'] = models.Section.objects.all()
	context['note_dates'] = models.Note.objects.dates('time', 'month', order='DESC')
	context['comments'] = comments.order_by('-comment_time')
	context['comment_form'] = CommentForm(
		initial={'content_type': note_content_type.model, 'object_id': note_id, 'reply_comment_id': 0})
	return render(request, 'note_detail.html', context)


def notes_with_section(request, section_id):
	context = {}
	note_section = get_object_or_404(models.Section, pk=section_id)
	# note_author=get_object_or_404(User,section_id)
	notes_all_list = models.Note.objects.filter(section=note_section)  # 获取当前section下所有的note
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
	if request.method == 'POST':
		new_title = request.POST.get('iname')
		new_time = request.POST.get('itime')
		new_content = request.POST.get('icontent', '')
		new_author = get_object_or_404(User, name=request.user)
		new_annex = request.POST.get('iannex')
		new_version = request.POST.get('iversion')
		new_note = models.Note(title=new_title, time=new_time, content=new_content, author=new_author, annex=new_annex,
		                       version=new_version)
		new_note.save()
		referer = request.META.get('HTTP_REFERER', reverse('home'))
		return redirect(referer)
	notes_all_version = models.Note.objects.filter(author=request.user)
	context = {}
	context['notes_all_version'] = notes_all_version
	return render(request, 'new_note.html', context)
