from django.db import models
from supportivelearning.models import StudentYear, Year, SubjectStudentYear
# Create your models here.
class Week(models.Model):
    SEMESTER_CHOICES=((1, "Semester 1"), (2, "Semester 2"),)
    TYPE_CHOICES=((True, "5 weeks"), (False, "Than 5 weeks"),)
    start=models.DateField()
    end=models.DateField()
    number=models.SmallIntegerField()
    type=models.BooleanField(choices=TYPE_CHOICES);
    semester=models.SmallIntegerField(choices=SEMESTER_CHOICES)
    year=models.ForeignKey(Year)
    student_year=models.ForeignKey(StudentYear)
    def __unicode__(self):
        return str(self.number)+" of " + self.get_type() 
    def get_type(self):
        if self.type:
            return "5 weeks"
        else:
            return "than 5 weeks"
    class Meta:
        verbose_name="Week"
class Holiday(models.Model):
    date=models.DateField()
    name=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name