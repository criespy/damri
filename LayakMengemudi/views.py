from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pemeriksaan, Pengemudi
from .forms import FormPengemudiCreate, FormPemeriksaanCreate, FormSetUpdatePengemudi, FormPemeriksaanTerakhir
from django.db.models import Count

def index(request):
    return render(request, 'home.html')

class Beranda(LoginRequiredMixin, TemplateView):
    login_url = 'auth/login'
    template_name = 'beranda.html'

class PengemudiCreate(LoginRequiredMixin, CreateView):
    model = Pengemudi
    template_name = 'pengemudi_createview.html'
    form_class = FormPengemudiCreate

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

    def get_queryset(self):
        id = self.kwargs['pk']
        return Pengemudi.objects.filter(pk=id)

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