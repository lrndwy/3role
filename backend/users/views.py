from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, guru, karyawan, siswa
from .serializers import UserSerializer, GuruSerializer, KaryawanSerializer, SiswaSerializer
from .permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import localtime
from .mixins import LogActivityMixin
from .models import guru, siswa, karyawan
# ... existing code ...

class UserViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)
        if role is not None:
            queryset = queryset.filter(role=role, is_active=True)
        return queryset

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class GuruViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = guru.objects.all()
    serializer_class = GuruSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('user'))
            if user.role != 'guru':
                return Response(
                    {'error': 'User harus memiliki role guru'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return super().create(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {'error': 'User tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

class KaryawanViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = karyawan.objects.all()
    serializer_class = KaryawanSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('user'))
            if user.role != 'karyawan':
                return Response(
                    {'error': 'User harus memiliki role karyawan'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return super().create(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {'error': 'User tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

class SiswaViewSet(LogActivityMixin, viewsets.ModelViewSet):
    queryset = siswa.objects.all()
    serializer_class = SiswaSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('user'))
            if user.role != 'siswa':
                return Response(
                    {'error': 'User harus memiliki role siswa'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return super().create(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {'error': 'User tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    # Ambil 10 log aktivitas terbaru
    latest_logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    
    activities = []
    for log in latest_logs:
        action = 'menambahkan' if log.action_flag == ADDITION else 'mengubah' if log.action_flag == CHANGE else 'menghapus'
        message = f"{log.user.username} {action} {log.content_type.model} - {log.object_repr}"
        activities.append({
            'id': log.id,
            'message': message,
            'time': log.action_time.strftime('%d %B %Y %H:%M')
        })

    stats = {
        'total_users': User.objects.count(),
        'total_guru': guru.objects.count(),
        'total_siswa': siswa.objects.count(),
        'total_karyawan': karyawan.objects.count(),
        'latest_activities': activities
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_users(request):
    # Dapatkan semua user dengan role yang diminta
    role = request.GET.get('role', '')
    
    # Dapatkan user yang sudah digunakan
    used_users = set()
    used_users.update(guru.objects.values_list('user_id', flat=True))
    used_users.update(siswa.objects.values_list('user_id', flat=True))
    used_users.update(karyawan.objects.values_list('user_id', flat=True))
    
    # Filter user yang belum digunakan dan sesuai role
    available_users = User.objects.filter(role=role).exclude(id__in=used_users)
    
    serializer = UserSerializer(available_users, many=True)
    return Response(serializer.data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        user_data = serializer.data

        # Tambahkan data spesifik berdasarkan peran
        if user.role == 'guru':
            try:
                guru_instance = guru.objects.get(user=user)
                user_data['nama'] = guru_instance.nama_guru
                user_data['nama_mapel'] = guru_instance.nama_mapel
            except guru.DoesNotExist:
                pass
        elif user.role == 'siswa':
            try:
                siswa_instance = siswa.objects.get(user=user)
                user_data['nama'] = siswa_instance.nama_siswa
                user_data['kelas'] = siswa_instance.kelas
            except siswa.DoesNotExist:
                pass
        elif user.role == 'karyawan':
            try:
                karyawan_instance = karyawan.objects.get(user=user)
                user_data['nama'] = karyawan_instance.nama_karyawan
                user_data['jabatan'] = karyawan_instance.jabatan
            except karyawan.DoesNotExist:
                pass

        return Response(user_data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        # Update user fields
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.address = data.get('address', user.address)
        user.tanggal_lahir = data.get('tanggal_lahir', user.tanggal_lahir)

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        # Handle file upload
        if 'foto_profil' in request.FILES:
            user.foto_profil = request.FILES['foto_profil']

        user.save()

        # Update role-specific fields
        if user.role == 'guru':
            guru_instance, created = guru.objects.get_or_create(user=user)
            guru_instance.nama_guru = data.get('nama', guru_instance.nama_guru)
            guru_instance.nama_mapel = data.get('nama_mapel', guru_instance.nama_mapel)
            guru_instance.save()
        elif user.role == 'siswa':
            siswa_instance, created = siswa.objects.get_or_create(user=user)
            siswa_instance.nama_siswa = data.get('nama', siswa_instance.nama_siswa)
            siswa_instance.kelas = data.get('kelas', siswa_instance.kelas)
            siswa_instance.save()
        elif user.role == 'karyawan':
            karyawan_instance, created = karyawan.objects.get_or_create(user=user)
            karyawan_instance.nama_karyawan = data.get('nama', karyawan_instance.nama_karyawan)
            karyawan_instance.jabatan = data.get('jabatan', karyawan_instance.jabatan)
            karyawan_instance.save()

        return Response(UserSerializer(user).data)
