# Generated by Django 4.1.2 on 2022-10-12 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LayakMengemudi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengemudi',
            name='status',
            field=models.CharField(choices=[('L', 'Layak Jalan'), ('TL', 'Tidak Layak Jalan')], default='TL', max_length=2),
        ),
    ]
