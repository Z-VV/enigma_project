from rest_framework import serializers
from .models import Signals

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signals
        fields = ('signal_type','symbol','buy_sell','stop_loss','take_profit','number','provider','created')

