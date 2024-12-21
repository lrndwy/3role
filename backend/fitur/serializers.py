from rest_framework import serializers
from .models import Galeri

class GaleriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeri
        fields = '__all__'