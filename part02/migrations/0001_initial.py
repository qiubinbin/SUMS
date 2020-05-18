# Generated by Django 3.0.2 on 2020-05-17 13:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
	initial = True

	dependencies = [
		('contenttypes', '0002_remove_content_type_name'),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name='Comment',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('object_id', models.PositiveIntegerField()),
				('content', models.TextField()),
				('comment_time', models.DateTimeField(auto_now_add=True)),
				('content_type',
				 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
				(
				'user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
			],
			options={
				'ordering': ['-comment_time'],
			},
		),
	]
