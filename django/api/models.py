from django.db import models
from datetime import datetime

# Create your models here.

class Signals(models.Model):
    signal_type = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    buy_sell = models.CharField(max_length=10)
    stop_loss = models.FloatField()
    take_profit = models.FloatField()
    number = models.IntegerField()
    provider = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.symbol



