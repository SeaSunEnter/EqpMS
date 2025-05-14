from django.db import models
from djmoney.models.fields import MoneyField

from manager.models import Customer


# Create your models here.

class AssetUnit(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AssetUnit'


class AssetCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AssetCategory'


class Asset(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=80)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # price = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    # price_depreciation = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    # input_date = models.DateField()
    # input_serial = models.CharField(max_length=10)
    # depreciation_date = models.DateField()
    # using_months = models.IntegerField()
    thumb = models.ImageField(blank=True, null=True, upload_to='Inventory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Asset'


class Inventory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    class Meta:
        db_table = 'Inventory'


