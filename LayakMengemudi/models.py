from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime
from django_resized import ResizedImageField
from django.utils import timezone

class Pengemudi(models.Model):
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(null=False, blank=False)#default=datetime.utcnow().date())
    kota_kelahiran = models.CharField(max_length=50, null=False, blank=False)
    alamat = models.TextField(null=False, blank=False)
    nik = models.CharField(max_length=16, null=False, blank=False, unique=True)
    nomor_hp = models.CharField(max_length=15, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    pendidikan_terakhir = models.CharField(max_length=6, null=True, blank=True)
    pool = models.CharField(max_length=50, null=True, blank=True)
    bus = models.CharField(max_length=6,null=True, blank=True)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Layak Jalan')
        TIDAK = 'TL', _('Tidak Layak Jalan')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)
    periksa_terakhir = models.DateTimeField(null=True)
    
    pasfoto = ResizedImageField(size=[300, 400], upload_to='images/%Y%m', default='images/no_pic.png')
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
    tanggal = models.DateTimeField(auto_now_add=True, blank=True)#.strftime("%Y-%m-%d %H:%M:%S"))
    #tensi = models.CharField(max_length=10)
    sistolik = models.IntegerField()
    diastolik = models.IntegerField()
    suhu = models.FloatField()
    jam_tidur = models.FloatField()
    gula_darah = models.FloatField(null=True, blank=True)
    kolesterol = models.FloatField(null=True, blank=True)
    class StatusAlkohol(models.TextChoices):
        TERDETEKSI = 'A', _('Terdeteksi Alkohol')
        TIDAK = 'NA', _('Tidak Terdeteksi Alkohol')
    #alkohol = models.CharField(max_length=2, choices=StatusAlkohol.choices, default=StatusAlkohol.TIDAK)
    alkohol = models.FloatField(null=True, blank=True)
    class StatusNapza(models.TextChoices):
        POSITIF = '+', _('Terdekteksi NAPZA')
        NEGATIF = '-', _('Tidak terdeteksi NAPZA')
    napza = models.CharField(max_length=1, choices=StatusNapza.choices, default=StatusNapza.NEGATIF)
    kondisi = models.CharField(max_length=200)
    class StatusJalan(models.TextChoices):
        LAYAK = 'L', _('Fit Mengemudi')
        TIDAK = 'TL', _('Tidak Fit')
    status = models.CharField(max_length=2, choices=StatusJalan.choices, default=StatusJalan.TIDAK)

    def __str__(self):
        return str(self.tanggal) + " - " + self.pengemudi.nama

    def get_absolute_url(self):
        return reverse('pengemudi-list')

    def save(self, *args, **kwargs):
        #hilangkan miliseconds saat save data
        current_datetime = timezone.now()
        current_datetime_without_milliseconds = current_datetime.replace(microsecond=0)
        self.tanggal = current_datetime_without_milliseconds

        super().save(*args, **kwargs)
        self.pengemudi.status = self.status
        self.pengemudi.periksa_terakhir = self.tanggal
        self.pengemudi.save()

    #def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)
    #    orang = Pengemudi.objects.get(id=self.pengemudi.id)
    #    orang.status = self.status
    #    orang.save(update_fields=['status'])