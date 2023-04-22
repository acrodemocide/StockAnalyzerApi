from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Stock(models.Model):
    businessName = models.CharField(max_length=100, blank=True, default='')
    ticker = models.CharField(max_length=10, blank=True, default='')
    price = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)

class Portfolio(models.Model):
    price_history = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    