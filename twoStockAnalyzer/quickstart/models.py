from django.db import models

# Models here
class Portfolio(models.Model):
    id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    #holdings = models.
    
    def __str__(self):
        return self.name