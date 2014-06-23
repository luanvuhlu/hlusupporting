from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

MAX_NOTIFICATION_CONTENT = 400
MAX_NAME_FIELD = 40
MAX_PHONE_FIELD = 15
MAX_YEAR_NAME_FIELD = 15
MAX_SUBJECT_NAME = 100
MAX_NOTE_FIELD = 200
MAX_CODE_FIELD = 7
MAX_STUDENT_YEAR_NAME_FIELD = 10
MAX_LOCATION_FIELD = 50
MAX_ROOM_FIELD = 10


class Notification(models.Model):
    content = models.CharField(max_length=MAX_NOTIFICATION_CONTENT)
    time = models.DateTimeField(default=datetime.now())
    read = models.BooleanField(default=False)


class StudentYear(models.Model):
    name = models.CharField(max_length=MAX_STUDENT_YEAR_NAME_FIELD, unique=True)
    note = models.CharField(max_length=MAX_NOTE_FIELD, blank=True)
    notifications = models.ManyToManyField(Notification, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Student Year"


class Student(models.Model):
    GENDER_CHOIES = ((0, "Female"), (1, "Male"),)
    user = models.OneToOneField(User)
    code = models.CharField(max_length=MAX_CODE_FIELD, blank=False, unique=True)
    student_year = models.ForeignKey(StudentYear)
    birthday = models.DateField(blank=True);
    gender = models.BooleanField(default=False, choices=GENDER_CHOIES)
    phone = models.CharField(max_length=MAX_PHONE_FIELD, blank=True)
    avarta = models.ImageField(upload_to="avarta", blank=True);
    notifications = models.ManyToManyField(Notification, blank=True)

    def __unicode__(self):
        return self.code;

    class Meta:
        verbose_name = "Student"
        ordering = ["-code", "-gender"]


class Year(models.Model):
    name = models.CharField(max_length=MAX_YEAR_NAME_FIELD)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Year"
        ordering = ["-name"]


class TimeTable(models.Model):
    SEMESTER_CHOICES = ((1, "Semester 1"), (2, "Semester 2"),)
    student = models.ForeignKey(Student)
    semester = models.SmallIntegerField(choices=SEMESTER_CHOICES)
    year = models.ForeignKey(Year)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = "TimeTable"


class Subject(models.Model):
    name = models.CharField(max_length=MAX_SUBJECT_NAME, unique=True)
    alias = models.CharField(max_length=MAX_SUBJECT_NAME)
    note = models.CharField(max_length=MAX_NOTE_FIELD, blank=True)
    description = models.TextField(blank=True);

    def __unicode__(self):
        return self.alias

    class Meta:
        verbose_name = "Subject"


class Faculity(models.Model):
    GENDER_CHOICES = ((0, "Female"), (1, "Male"),)
    first_name = models.CharField(max_length=MAX_NAME_FIELD)
    last_name = models.CharField(max_length=MAX_NAME_FIELD)
    email = models.EmailField(blank=True);
    phone = models.CharField(max_length=MAX_PHONE_FIELD, blank=True)
    gender = models.BooleanField(default=False, choices=GENDER_CHOICES)
    avarta = models.FileField(upload_to="avarta", blank=True);

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Faculity"


class FaculitySubject(models.Model):
    faculity = models.ForeignKey(Faculity)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return self.subject.name + " " + self.faculity.last_name

    class Meta:
        verbose_name = "Faculity Subject"


class SubjectStudentYear(models.Model):
    NUMBER_WEEK = ( (5, '5 weeks'),
                    (15, '15 weeks'),
                    (12, 'other'),
    )
    NUMBER_CHOICES = (
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    subject = models.ForeignKey(Subject)
    student_year = models.ForeignKey(StudentYear)
    year = models.ForeignKey(Year)
    week_number = models.SmallIntegerField(choices=NUMBER_WEEK, default=5)
    days_in_week = models.SmallIntegerField(default=2, choices=NUMBER_CHOICES)
    note = models.CharField(max_length=MAX_NOTE_FIELD, blank=True)

    def __unicode__(self):
        return self.subject.name + " " + self.student_year.name + " " + self.year.name

    class Meta:
        verbose_name = "Subject Student Year"


class TimeTableSubject(models.Model):
    subject = models.ForeignKey(SubjectStudentYear)
    timetable = models.ForeignKey(TimeTable)
    start = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return self.subject.subject.alias

    class Meta:
        verbose_name = "TimeTable Subject"


# class Message(models.Model):
# TYPE_MESSAGE=((1, "Warn"),
#                   (2, "Error"),
#                   )
#     content=models.TextField()
#     type=models.SmallIntegerField(choices=TYPE_MESSAGE)
#     actived=models.BooleanField()
#     def get_type(self):
#         for tup in self.TYPE_MESSAGE:
#             if(tup[0]==self.type):
#                 return tup[1]
#     def __unicode__(self):
#         return self.content;
#     class Meta:
#         verbose_name="Message"
class Day(models.Model):
    WEEK_DAY_CHOICES = ((1, "Monday"),
                        (2, "Tuesday"),
                        (3, "Wednesday"),
                        (4, "Thursday"),
                        (5, "Friday"),
                        (6, "Saturday"),)
    LOCATION_CHOICES = (("A", "A"),
                        ("B", "B"),
                        ("C", "C"),
                        ("D", "D"),
                        ("E", "E"),
                        ("F", "F"),
                        ("G", "G"),
    )
    NUMBER_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    TYPE_CHOICES = ((False, "Theory"), (True, "Seminar"), )
    week_day = models.SmallIntegerField(choices=WEEK_DAY_CHOICES)
    location = models.CharField(max_length=MAX_LOCATION_FIELD, choices=LOCATION_CHOICES)
    room = models.CharField(max_length=MAX_ROOM_FIELD)
    start_hour = models.SmallIntegerField()
    end_hour = models.SmallIntegerField()
    timetable_subject = models.ForeignKey(TimeTableSubject)
    type = models.BooleanField(default=False, choices=TYPE_CHOICES)
    number = models.SmallIntegerField(default=1, choices=NUMBER_CHOICES)

    def __unicode__(self):
        for tup in self.NUMBER_CHOICES:
            if (tup[0] == self.number):
                return tup[1]

    class Meta:
        verbose_name = "Day"
        # class DayCalendar(models.Model):
        #     CATEGORIES_CHOICES=(
        #                         (0, "Subject"),
        #                         (1, "Other"),
        #                         )
        #     user=models.ForeignKey(User)
        #     name=models.CharField(max_length=150)
        #     content=models.CharField(max_length=200)
        #     category=models.SmallIntegerField(default=0, choices=CATEGORIES_CHOICES)
        #     day=models.DateField()