from django.db import models

# Models here
class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    
    #def __str__(self):
    #    return self.name

class User(models.Model):
    name = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=50)