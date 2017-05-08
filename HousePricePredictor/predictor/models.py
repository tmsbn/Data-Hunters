from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Models for house data
class HouseData(models.Model):
    no = models.IntegerField(primary_key=True)
    land_use = models.CharField(max_length=30)
    sold_as_vacant = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    square_footage = models.PositiveIntegerField(default=0,
                                                 validators=[
                                                     MaxValueValidator(10000000),
                                                     MinValueValidator(0)
                                                 ])
    tax_district = models.CharField(max_length=50)
    neighborhood = models.PositiveIntegerField(default=0,
                                               validators=[
                                                   MaxValueValidator(10000000),
                                                   MinValueValidator(0)
                                               ])
    land_value = models.PositiveIntegerField(default=0,
                                             validators=[
                                                 MaxValueValidator(10000000),
                                                 MinValueValidator(0)
                                             ])
    sales_price = models.IntegerField(default=0)
