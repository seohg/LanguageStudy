from django.db import models

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=200)
    images = models.ImageField(upload_to='static/images', null=True)
'''
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
'''
