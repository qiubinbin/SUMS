from django import forms


class NewNoteFiles(forms.Form):
	"""附件"""
	annex = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  # 附件
