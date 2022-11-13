from django.db import models
from django.utils.translation import gettext_lazy as _

class Pengemudi(models.Model):
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=12)
    pool = models.CharField(max_length=50)
    bus = models.CharField(max_length=6)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Layak Jalan')
        TIDAK = 'TL', _('Tidak Layak Jalan')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)
    periksa_terakhir = models.DateTimeField(null=True)
    qrcode_path = models.CharField(max_length=256, default="none")

    def __str__(self):
        return self.nama

class Pemeriksaan(models.Model):
    pengemudi = models.ForeignKey(Pengemudi, on_delete=models.CASCADE)
    tanggal = models.DateTimeField()
    tensi = models.CharField(max_length=10)
    suhu = models.FloatField()
    jam_tidur = models.FloatField()
    kondisi = models.CharField(max_length=200)

    def __str__(self):
        return self.tanggal + " - " + self.pengemudi
