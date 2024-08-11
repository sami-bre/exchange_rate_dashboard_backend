from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exchange
from .serializers import ExchangeDetailSerializer, GroupedExchangeSerializer

class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeDetailSerializer

    @action(detail=False, methods=['get'])
    def grouped(self, request):
        queryset = self.get_queryset().order_by('currency_name', 'bank_name', 'created_at')
        serializer = GroupedExchangeSerializer(queryset)
        return Response(serializer.data)