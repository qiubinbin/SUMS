from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist


class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
	                          error_messages={'required':'审批意见不能为空！',})

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')  # 从 **kwargs取出user
		super().__init__(*args, **kwargs)

	def clean(self):
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user
		else:
			raise forms.ValidationError('用户未登录！')
		content_type = self.cleaned_data['content_type']
		object_id = self.cleaned_data['object_id']
		try:
			model_class = ContentType.objects.get(model=content_type).model_class()
			model_obj = model_class.objects.get(pk=object_id)
			self.cleaned_data['content_object'] = model_obj
		except ObjectDoesNotExist:
			raise forms.ValidationError('对象不存在！')
		return self.cleaned_data
