from django.db import models


# Create your models here.
class HouseData(models.Model):
    no = models.IntegerField(primary_key=True)
    land_use = models.CharField(max_length=20)
    sold_as_vacant = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    square_footage = models.IntegerField(default=0)
    tax_district = models.CharField(max_length=20)
    neighborhood = models.IntegerField(default=0)
    land_value = models.IntegerField(default=0)
    sales_price = models.IntegerField(default=0)
