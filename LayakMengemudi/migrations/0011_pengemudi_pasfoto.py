# Generated by Django 4.1.3 on 2022-11-23 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LayakMengemudi', '0010_alter_pengemudi_pasfoto_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengemudi',
            name='pasfoto',
            field=models.ImageField(default='belum ada', upload_to='images/'),
            preserve_default=False,
        ),
    ]
