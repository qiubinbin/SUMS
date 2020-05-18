# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Comment


def submit_comment(request):
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	if not request.user.is_authenticated:
		return render(request, 'error.html', {'message': '用户未登录！', 'redirect_to': referer})
	content = request.POST.get('text', '').strip()
	if not content:
		return render(request, 'error.html', {'message': '意见为空！', 'redirect_to': referer})
	try:
		content_type = request.POST.get('content_type', '')
		object_id = int(request.POST.get('object_id', ''))
		model_class = ContentType.objects.get(model=content_type).model_class()
		model_obj = model_class.objects.get(pk=object_id)
	except Exception as e:
		print(referer)
		return render(request, 'error.html', {'message': '对象不存在！', 'redirect_to': referer})
	# 检查无误，新的审批意见
	comment = Comment()
	comment.user = request.user
	comment.content = content
	comment.content_object = model_obj
	comment.save()
	print(referer)
	return redirect(referer)
