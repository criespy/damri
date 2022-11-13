from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pemeriksaan, Pengemudi

def index(request):
    return render(request, 'home.html')

class Beranda(LoginRequiredMixin, TemplateView):
    login_url = 'auth/login'
    template_name = 'beranda.html'

class PengemudiDetail(DetailView):
    model = Pengemudi
    template_name = 'pengemudi_detail.html'

class PemeriksaanCreate(CreateView):
    model = Pemeriksaan
    template_name = 'pemeriksaan_create.html'