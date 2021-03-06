# Create your views here.
from django.http import JsonResponse
from django.urls import reverse

from .forms import CommentForm
from .models import Comment


def submit_comment(request):
	'''referer = request.META.get('HTTP_REFERER', reverse('home'))
	if not request.user.is_authenticated:
		return render(request, 'error.html', {'message': '用户未登录！', 'redirect_to': referer})
	content = request.POST.get('content', '').strip()
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
	return redirect(referer)'''
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	comment_form = CommentForm(request.POST, user=request.user)
	data = {}
	if comment_form.is_valid():
		comment = Comment()
		comment.user = comment_form.cleaned_data['user']
		comment.content = comment_form.cleaned_data['content']
		comment.content_object = comment_form.cleaned_data['content_object']
		parent = comment_form.cleaned_data['parent']
		if parent:
			comment.root = parent.root if parent.root else parent
			comment.parent = parent
			comment.parent_name = parent.user
		comment.save()
		# 返回数据
		data['status'] = 'SUCCESS'
		data['username'] = comment.user.username
		data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
		data['content'] = comment.content
		if parent:
			data['parent_name'] = comment.parent_name.username
		else:
			data['parent_name'] = ''
		data['pk'] = comment.pk
		data['root_pk']=comment.root.pk if comment.root else ''

	else:
		# return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
		data['status'] = 'ERROR'
		data['message'] = list(comment_form.errors.values())[0]
	return JsonResponse(data)
