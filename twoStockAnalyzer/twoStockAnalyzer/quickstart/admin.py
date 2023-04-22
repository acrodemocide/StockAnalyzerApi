from django.contrib import admin
#from . import models# import Portfolio
from .models import Portfolio

# Register your models here.
admin.site.register(Portfolio)