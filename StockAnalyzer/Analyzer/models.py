from django.db import models

# Create your models here.

class Stock(models.Model):
    businessName = models.CharField(max_length=100, blank=True, default='')
    ticker = models.CharField(max_length=10, blank=True, default='')
    price = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)