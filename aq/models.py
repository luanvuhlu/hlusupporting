from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
MAX_SHORT_QUESTION_ANSWER=200
class Tag(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=400, blank=True)
    def __unicode__(self):
        return self.name
class Answer(models.Model):
    user=models.ForeignKey(User)
    content=models.TextField()
    time=models.DateTimeField(default=datetime.now())
    def __unicode__(self):
        return self.content
class Question(models.Model):
	STATUS_CHOICE=(
				(-1, "Closed"),
				(0, "Default"),
				(1, "Solved"),
				(2, "Duplicated"),
				)
	tags=models.ManyToManyField(Tag)
	content=models.TextField()
	user=models.ForeignKey(User)
	time=models.DateTimeField(default=datetime.now())
	status=models.SmallIntegerField(choices=STATUS_CHOICE, default=0)
	def __uncode__(self):
		return self.content
