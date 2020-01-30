from django.db import models

# Create your models here.
class Address(models.Model):
    address_line_1 = models.CharField(max_length=125)
    address_line_2 = models.CharField(max_length=125)
    address_line_3 = models.CharField(max_length=125)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=16)