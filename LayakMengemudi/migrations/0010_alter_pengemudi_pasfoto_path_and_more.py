# Generated by Django 4.1.3 on 2022-11-23 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LayakMengemudi', '0009_alter_pengemudi_alamat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pengemudi',
            name='pasfoto_path',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pengemudi',
            name='qrcode_path',
            field=models.CharField(max_length=256),
        ),
    ]