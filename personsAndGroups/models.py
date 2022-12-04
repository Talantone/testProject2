from django.db import models


class Person(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=255)


class Group(models.Model):
    name = models.CharField(max_length=255)
    persons = models.ManyToManyField(Person)


