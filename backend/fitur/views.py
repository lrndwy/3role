from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Galeri
from .serializers import GaleriSerializer

class GaleriViewSet(viewsets.ModelViewSet):
    queryset = Galeri.objects.all()
    serializer_class = GaleriSerializer
    permission_classes = [IsAuthenticated]