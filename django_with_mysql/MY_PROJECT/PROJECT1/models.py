from django.db import models

# Create your models here.

class details(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    year_of_joining=models.IntegerField(default=0)
    depart=models.CharField(max_length=20,default="")
    email=models.CharField(max_length=50)

class student(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    std=models.CharField(max_length=20)
    grade=models.CharField(max_length=20)

class user(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=50)




