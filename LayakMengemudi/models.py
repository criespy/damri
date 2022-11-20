from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime

class Pengemudi(models.Model):
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(default=datetime.utcnow().date())
    kota_kelahiran = models.CharField(max_length=50, default="none", null=False)
    alamat = models.TextField(default="none", null=False)
    nik = models.CharField(max_length=12)
    pool = models.CharField(max_length=50)
    bus = models.CharField(max_length=6)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Layak Jalan')
        TIDAK = 'TL', _('Tidak Layak Jalan')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)
    periksa_terakhir = models.DateTimeField(null=True)
    pasfoto_path = models.CharField(max_length=256, default="none")
    qrcode_path = models.CharField(max_length=256, default="none")

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
        return self.tanggal + " - " + self.pengemudi

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        orang = Pengemudi.objects.get(id=self.pengemudi.id)
        orang.status = self.status
        orang.save(update_fields=['status'])