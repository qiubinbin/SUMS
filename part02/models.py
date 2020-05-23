from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	content = models.TextField()
	comment_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)  # 评论人
	root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
	parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
	parent_name = models.ForeignKey(User, related_name='reply', null=True, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.content

	class Meta:
		ordering = ['-comment_time']
