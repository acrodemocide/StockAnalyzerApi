from django.db import models
# from pygments.lexers import get_all_lexers
# from pygments.styles import get_all_styles

# Create your models here.
# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Stock(models.Model):
    businessName = models.CharField(max_length=100, blank=True, default='')
    ticker = models.CharField(max_length=10, blank=True, default='')
    price = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)