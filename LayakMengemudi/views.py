from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pemeriksaan, Pengemudi
from .forms import FormPengemudiCreate

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

class PemeriksaanCreate(LoginRequiredMixin, CreateView):
    model = Pemeriksaan
    template_name = 'pemeriksaan_create.html'