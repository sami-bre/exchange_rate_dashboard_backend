from rest_framework import serializers
from .models import Exchange

class ExchangeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ['id', 'currency_name', 'bank_name', 'buy_rate', 'sell_rate', 'increment_amount', 'created_at', 'updated_at']


class GroupedExchangeSerializer(serializers.Serializer):
    def to_representation(self, queryset):
        result = {}
        for exchange in queryset:
            if exchange.currency_name not in result:
                result[exchange.currency_name] = {}
            if exchange.bank_name not in result[exchange.currency_name]:
                result[exchange.currency_name][exchange.bank_name] = []
            result[exchange.currency_name][exchange.bank_name].append(
                ExchangeDetailSerializer(exchange).data
            )
        return result