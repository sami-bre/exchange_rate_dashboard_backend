from rest_framework import viewsets
from .models import Exchange
from .serializers import ExchangeSerializer

class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer