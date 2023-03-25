# Generated by Django 4.1.7 on 2023-03-24 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LayakMengemudi', '0016_pemeriksaan_alkohol_pemeriksaan_gula_darah_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengemudi',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='pengemudi',
            name='nomor_hp',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='pengemudi',
            name='pendidikan_terakhir',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
