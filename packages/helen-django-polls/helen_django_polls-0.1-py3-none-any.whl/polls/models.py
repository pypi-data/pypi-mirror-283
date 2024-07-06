from django.contrib import admin
from django.utils import timezone

from django.db import models


class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

    # ...
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        one_day_ago = now - timezone.timedelta(days=1)
        return one_day_ago <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
