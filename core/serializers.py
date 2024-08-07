from rest_framework import serializers
from .models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ['id', 'currency_name', 'bank_name', 'buy_rate', 'sell_rate', 'increment_amount', 'created_at', 'updated_at']