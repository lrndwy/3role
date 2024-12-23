# Generated by Django 5.1.4 on 2024-12-11 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_guru_karyawan_siswa'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='foto_profil',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='user',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True),
        ),
    ]
