from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Badge(models.Model):
    badge = models.TextField()

class Skill(models.Model):
    skill = models.TextField()

class User(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    name = models.TextField()
    password = models.TextField()
    points = models.IntegerField()
    email = models.TextField()
    badge = models.ManyToManyField(Badge)
    skills = models.ManyToManyField(Skill)

class Tag(models.Model):
    tag = models.TextField()

class Question(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    createdOn = models.DateTimeField(default=timezone.now)
    tag = models.ManyToManyField(Tag)

class Answer(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    votes = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    createdOn = models.DateTimeField(default=timezone.now)
