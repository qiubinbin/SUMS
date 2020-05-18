# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Comment


def submit_comment(request):
	user = request.user
	content = request.POST.get('text', '').strip()
	if not content:
		return render(request, '#')  # TODO
	content_type = request.POST.get('content_type', '')
	object_id = int(request.POST.get('object_id', ''))
	model_class = ContentType.objects.get(model=content_type).model_class()
	model_obj = model_class.objects.get(pk=object_id)
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	comment = Comment()
	comment.user = user
	comment.content = content
	comment.content_object = model_obj
	comment.save()
	return redirect(referer)
