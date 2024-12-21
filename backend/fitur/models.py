from django.db import models

class Galeri(models.Model):
    KATEGORI_CHOICES = [
        ('kegiatan', 'Kegiatan'),
        ('prestasi', 'Prestasi'),
        ('fasilitas', 'Fasilitas'),
        ('lainnya', 'Lainnya'),
    ]
    
    foto = models.ImageField(upload_to='galeri/')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    tanggal = models.DateField()
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-tanggal']
        verbose_name_plural = 'Galeri'

    def __str__(self):
        return self.judul