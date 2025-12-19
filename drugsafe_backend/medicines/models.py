from django.db import models
from django.conf import settings

# Create your models here.
class Form(models.Model):
  name = models.TextField()

class Symptom(models.Model):
  name = models.TextField()

class Drug(models.Model):
  symptom = models.ForeignKey(Symptom, related_name='symptoms', on_delete=models.CASCADE)
  form = models.ForeignKey(Form, related_name='forms_drug', on_delete=models.CASCADE)
  name = models.TextField()
  company = models.TextField()
  basis = models.TextField()
  efficacy = models.TextField()
  use = models.TextField()
  description = modeles.TextField()
  caution = models.TextField()
  caution_intake = models.TextField()
  side_effect = models.TextField()
  store = models.TextField()

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  drug = models.ForeignKey(Drug, related_name='drugs', on_delete=models.CASCADE)
  form = models.ForeignKey(Form, related_name='forms_review', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Score(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    score = models.IntegerField()

class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)