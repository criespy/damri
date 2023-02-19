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

def index(request):
    return render(request, 'home.html')

class Beranda(LoginRequiredMixin, TemplateView):
    login_url = 'auth/login'
    template_name = 'beranda.html'

class PengemudiCreate(LoginRequiredMixin, CreateView):
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
    model = Pengemudi
    template_name = 'pengemudi_updateview.html'
    form_class = FormPengemudiCreate

class PengemudiList(LoginRequiredMixin, ListView):
    model = Pengemudi
    template_name = 'pengemudi_listview.html'

class PengemudiDetail(LoginRequiredMixin,DetailView):
    model = Pengemudi
    template_name = 'pengemudi_detailview.html'
    slug_field = 'nik'

    def get_queryset(self):
        id = self.kwargs['slug']
        return Pengemudi.objects.filter(nik=id)

    def get_context_data(self, **kwargs):
        detail = super(PengemudiDetail, self).get_context_data(**kwargs)
        #Queryset
        #detail['periksaTerakhir'] = Pengemudi.objects.annotate(periksa_count=Count('pemeriksaan')).filter(periksa_count=0)
        if self.request.POST:
            #detail['form'] = FormPemeriksaanCreate(self.request.POST, instance=self.object)
            detail['konteks'] = FormPemeriksaanTerakhir (
                self.request.POST, instance=self.object)
        else:
            #detail['form'] = FormPemeriksaanCreate(instance=self.object)
            detail['konteks'] = FormPemeriksaanTerakhir(instance=self.object)
        return detail

class PemeriksaanCreate(LoginRequiredMixin, CreateView):
    model = Pemeriksaan
    template_name = 'pemeriksaan_createview2.html'
    form_class = FormPemeriksaanCreate

class PemeriksaanUpdate(LoginRequiredMixin, UpdateView):
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
    model = Pemeriksaan
    template_name = 'pemeriksaan_listview'

class PrintIDCard(LoginRequiredMixin, DetailView):
    model = Pengemudi
    template_name = 'pengemudi_printview.html'
    slug_field = 'nik'