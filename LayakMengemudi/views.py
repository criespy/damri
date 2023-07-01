from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pemeriksaan, Pengemudi
from .forms import FormPengemudiCreate, FormPemeriksaanCreate, FormSetUpdatePengemudi, FormPemeriksaanTerakhir
#from django.utils import timezone
#import datetime
#from django.db.models import Count
import qrcode
from pathlib import os
from django.db.models.expressions import RawSQL
from datetime import datetime, date
#import datetime
from django.db.models import Q
from django.utils.timezone import timedelta

def index(request):
    return render(request, 'home.html')

class Beranda(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'beranda.html'

class PengemudiCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pengemudi_createview.html'
    form_class = FormPengemudiCreate

    def form_valid(self, form):
        qrcode = form.cleaned_data['nik']
        self.valid_submission_callback(qrcode)
        return super(PengemudiCreate, self).form_valid(form)

    def valid_submission_callback(self, data):
        input_data = data
        qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=2)
        qr.add_data(input_data)
        qr.make(fit=True)
        #img = qr.make_image(fill='black', back_color='white')
        #img.save('.'+static('/images/part_qrcodes/' + data + '.png'))
        img = qr.make_image(fill='black', back_color='white')
        imgfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/qrcodes/' + data + '.png')
        img.save((imgfile))

class PengemudiUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pengemudi_updateview.html'
    form_class = FormPengemudiCreate

class PengemudiList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pengemudi_listview.html'

    def get_queryset(self):
        q = "SELECT *, cast(round((julianday('now') - julianday(tanggal_lahir)) / 365) as int) as usia FROM LayakMengemudi_pengemudi"

        #raw = 'Select DATEDIFF(CURDATE(), `yourappname_patienttable`.`dob`) from `yourappname_patienttable` u where u.`id`=`yourappname_patienttable`.id'

        #return Pengemudi.objects.all().annotate(usia=RawSQL(raw, ()))#filter(id=1)
        return Pengemudi.objects.raw(q)

class PengemudiDetail(LoginRequiredMixin,DetailView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pengemudi_detailview.html'
    slug_field = 'nik'

    def get_queryset(self):
        id = self.kwargs['slug']
        return Pengemudi.objects.all() #filter(nik=id)

    def get_context_data(self, **kwargs):
        #metode yang diambil dari aparApp
        context = super().get_context_data(**kwargs)
        pengemudi = self.get_object()
        pemeriksaan_list = Pemeriksaan.objects.filter(pengemudi_id=pengemudi).order_by('-tanggal')
        context['pemeriksaan_list'] = pemeriksaan_list
        #Queryset (metode sebelum aparApp)
        detail = super(PengemudiDetail, self).get_context_data(**kwargs)
        #detail['periksaTerakhir'] = Pengemudi.objects.annotate(periksa_count=Count('pemeriksaan')).filter(periksa_count=0)
        if self.request.POST:
            #detail['form'] = FormPemeriksaanCreate(self.request.POST, instance=self.object)
            detail['konteks'] = FormPemeriksaanTerakhir (
                self.request.POST, instance=self.object, queryset=Pemeriksaan.objects.order_by('tanggal')) #belum fix, supaya ditampilkan hasil periksa terakhir
        else:
            #detail['form'] = FormPemeriksaanCreate(instance=self.object)
            detail['konteks'] = FormPemeriksaanTerakhir(instance=self.object)
        return context

class PemeriksaanCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Pemeriksaan
    template_name = 'pemeriksaan_createview2.html'
    form_class = FormPemeriksaanCreate

class PemeriksaanUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pemeriksaan_createview.html'
    form_class = FormPemeriksaanCreate

    def get_queryset(self):
        id = self.kwargs['pk']
        return Pengemudi.objects.filter(pk=id)

    def get_context_data(self, **kwargs):
        detail = super(PemeriksaanCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            detail['form'] = FormPemeriksaanCreate(self.request.POST, instance=self.object)
            detail['konteks'] = FormSetUpdatePengemudi(
                self.request.POST, instance=self.object)
        else:
            detail['form'] = FormPemeriksaanCreate(instance=self.object)
            detail['konteks'] = FormSetUpdatePengemudi(instance=self.object)

        return detail

class PemeriksaanList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Pemeriksaan
    template_name = 'pemeriksaan_listview'

class PrintIDCard(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Pengemudi
    template_name = 'pengemudi_printview.html'
    slug_field = 'nik'

class ReportView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    model = Pemeriksaan
    template_name = 'report_generalview.html'

class ReportPemeriksaanHarian(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Pemeriksaan
    template_name = 'report_pemeriksaan_harian.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        daritanggal = self.request.GET.get('fromDate') #datetime(2023, 6, 30, 0, 0, 0)#datetime.now().date()#datetime.date.today()
        sampaitanggal = self.request.GET.get('toDate') #datetime(2023, 6, 30, 23, 59, 59)
        if daritanggal and sampaitanggal:
            daritanggal = datetime.strptime(daritanggal, '%Y-%m-%d')
            sampaitanggal = datetime.strptime(sampaitanggal, '%Y-%m-%d') + timedelta(days=1) #supaya include hari berjalan pakai timedelta
            queryset = queryset.filter(tanggal__range=(daritanggal, sampaitanggal))

        return queryset #Pemeriksaan.objects.filter(Q(tanggal__gte = daritanggal) & Q(tanggal__lte = sampaitanggal)).order_by('tanggal')
    #Pemeriksaan.objects.filter(tanggal__range = (daritanggal, sampaitanggal)).order_by('tanggal')  #Pemeriksaan.objects.filter(tanggal__date = daritanggal)#
    