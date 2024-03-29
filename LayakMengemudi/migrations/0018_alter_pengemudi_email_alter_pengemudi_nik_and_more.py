# Generated by Django 4.1.7 on 2023-03-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LayakMengemudi', '0017_pengemudi_email_pengemudi_nomor_hp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pengemudi',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pengemudi',
            name='nik',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='pengemudi',
            name='nomor_hp',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
