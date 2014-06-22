from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Tags(models.Model):
	name=models.CharField(max_lerngth=100)
	desctiption=models.CharField(max_length=200, blank=False)
class TagAlias(models.Model):
		alias=models.ForeignKey(Tags)
class Anwser(models.Model):
	content=models.TextField()
	time=models.DateTimeField(default=datetime.now())
class Question(models.Model):
	STATUS_CHOICE=(
				(-1, "Closed"),
				(0, "Default"),
				(1, "Solved"),
				(2, "Duplicated"),
				)
	tasalias=models.ManyToManyField(TagAlias)
	content=models.TextField()
	user=models.ForeignKey(User)
	time=models.DateTimeField(default=datetime.now())
	status=models.SmallIntegerField(choices=STATUS_CHOICE, default=0)
class CommentAnwser(models.Model):
	anwser=models.ForeignKey(Anwser)
	content=models.CharField(max_length=400)
	user=models.ForeignKey(User)
	time=models.DateTimeField(default=datetime.now())
class QuestionNote(models.Model):
	question=models.ForeignKey(Question)
	content=models.CharField(max_length=400)
	user=models.ForeignKey(User)
	time=models.DateTimeField(default=datetime.now())