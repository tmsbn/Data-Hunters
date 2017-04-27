from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class HouseData(models.Model):
    no = models.IntegerField(primary_key=True)
    land_use = models.CharField(max_length=20)
    sold_as_vacant = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    square_footage = models.PositiveIntegerField(default=0,
                                                 validators=[
                                                     MaxValueValidator(1000000),
                                                     MinValueValidator(0)
                                                 ])
    tax_district = models.CharField(max_length=20)
    neighborhood = models.PositiveIntegerField(default=0,
                                               validators=[
                                                   MaxValueValidator(1000000),
                                                   MinValueValidator(0)
                                               ])
    land_value = models.PositiveIntegerField(default=0,
                                             validators=[
                                                 MaxValueValidator(1000000),
                                                 MinValueValidator(0)
                                             ])
    sales_price = models.IntegerField(default=0)
