from django.db import models
from supportivelearning.models import SubjectStudentYear
# Create your models here.
class Document(models.Model):
    subject=models.ForeignKey(SubjectStudentYear)
    decription=models.TextField(blank=True)
    def __unicode__(self):
        return str(self.subject)
class DocumentLearning(models.Model):
    TYPE_CHOICES=(
                  (0, "Books"),
                  (1, "Law"),
                  (2, "Website")
                  )
    name=models.CharField(max_length=200)
    type=models.SmallIntegerField(default=0, choices=TYPE_CHOICES)
    document=models.ForeignKey(Document)
class Week(models.Model):
    number=models.SmallIntegerField()
    note=models.CharField(max_length=100, blank=True)
    require=models.TextField(blank=True)
    document=models.ForeignKey(Document)
    def __unicode__(self):
        return str(self.number)
class Day(models.Model):
    TYPE_CHOICES=(
                  (False, "Theory"),
                  (True, "Seminar")
                  )
    NUMBER_CHOICES=(
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    )
    type=models.BooleanField(default=False, choices=TYPE_CHOICES)
    number=models.SmallIntegerField(choices=NUMBER_CHOICES, blank=True)
    content=models.TextField(blank=True)
    note=models.CharField(max_length=200, blank=True)
    week=models.ForeignKey(Week)
    def __unicode__(self):
        if self.type:
            return "Seminar "+str(self.number)
        else:
            return "Theory "+str(self.number)
class HomeWork(models.Model):
    TYPE_CHOICES=(
                  (0, "Person"),
                  (1, "Group"),
                  (2, "Final")
                  )
    REQUIRE_CHOICES=(
                     (None, "Anything"),
                     (False, "Hand"),
                     (True, "Print")
                     )
    type=models.SmallIntegerField(choices=TYPE_CHOICES)
    require=models.NullBooleanField(choices=REQUIRE_CHOICES)
    pages=models.CharField(max_length=30)
    document=models.ForeignKey(Document)