from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('karyawan', 'Karyawan'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    foto_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'users' 
    

        
class guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guru')
    nama_guru = models.CharField(max_length=100)
    nama_mapel = models.CharField(max_length=100)
    class Meta:
        db_table = 'guru'
        
class siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='siswa')
    nama_siswa = models.CharField(max_length=100)
    kelas = models.CharField(max_length=100)
    class Meta:
        db_table = 'siswa'
        
class karyawan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='karyawan')
    nama_karyawan = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    class Meta:
        db_table = 'karyawan'
