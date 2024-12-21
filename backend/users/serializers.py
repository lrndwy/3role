from rest_framework import serializers
from .models import User, guru, karyawan, siswa
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    foto_profil_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'is_active', 'foto_profil', 'foto_profil_url', 'address', 'tanggal_lahir', 'phone')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'foto_profil': {'required': False}
        }

    def get_foto_profil_url(self, obj):
        try:
            if obj.foto_profil and hasattr(obj.foto_profil, 'url'):
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(obj.foto_profil.url)
                return obj.foto_profil.url
        except Exception as e:
            print(f"Error getting foto_profil_url: {str(e)}")
        return None

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    def update(self, instance, validated_data):
        if 'password' in validated_data and validated_data['password']:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class GuruSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = guru
        fields = ('id', 'user', 'user_detail', 'nama_guru', 'nama_mapel')

class KaryawanSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = karyawan
        fields = ('id', 'user', 'user_detail', 'nama_karyawan', 'jabatan')

class SiswaSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = siswa
        fields = ('id', 'user', 'user_detail', 'nama_siswa', 'kelas')
