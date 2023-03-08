from django.db import models

# Models here
class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    # name = models.CharField(max_length=256)
    # b_and_h_value = models.FloatField(max_value=None, min_value=0)
    # tactical_rebal_value = models.FloatField(max_value=None, min_value=0)
    # b_and_h_allocation = models.ListField(child=models.FloatField(min_value=0))
    # tactical_rebal_allocation = models.ManyToOneRel(child=models.FloatField(min_value=0))
    # bh_graph_data = models.ListField(child=models.FloatField(min_value=0))
    # tr_graph_data = models.ListField(child=models.FloatField(min_value=0))
    # holdings = models.ListField(child=models.CharField(max_length=10))