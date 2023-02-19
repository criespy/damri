from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime
from django_resized import ResizedImageField

class Pengemudi(models.Model):
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(null=False, blank=False)#default=datetime.utcnow().date())
    kota_kelahiran = models.CharField(max_length=50, null=False, blank=False)
    alamat = models.TextField(null=False, blank=False)
    nik = models.CharField(max_length=12, null=False, blank=False)
    pool = models.CharField(max_length=50)
    bus = models.CharField(max_length=6)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Layak Jalan')
        TIDAK = 'TL', _('Tidak Layak Jalan')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)
    periksa_terakhir = models.DateTimeField(null=True)
    
    pasfoto = ResizedImageField(size=[200, 150],upload_to='images/%Y/%Y%m%d.png')
    qrcode_path = models.CharField(max_length=256)

    def f(instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            return '{}.{}'.format(instance.pk, ext)
        else:
            pass

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('pengemudi-list')

class Pemeriksaan(models.Model):
    pengemudi = models.ForeignKey(Pengemudi, on_delete=models.CASCADE)
    tanggal = models.DateTimeField()
    tensi = models.CharField(max_length=10)
    suhu = models.FloatField()
    jam_tidur = models.FloatField()
    kondisi = models.CharField(max_length=200)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Layak Jalan')
        TIDAK = 'TL', _('Tidak Layak Jalan')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)

    def __str__(self):
        return str(self.tanggal) + " - " + self.pengemudi.nama

    def get_absolute_url(self):
        return reverse('pengemudi-list')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pengemudi.status = self.status
        self.pengemudi.periksa_terakhir = self.tanggal
        self.pengemudi.save()

    #def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)
    #    orang = Pengemudi.objects.get(id=self.pengemudi.id)
    #    orang.status = self.status
    #    orang.save(update_fields=['status'])