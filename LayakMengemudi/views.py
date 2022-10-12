from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from .models import Pemeriksaan, Pengemudi

def index(request):
    return render(request, 'home.html')

class PengemudiDetail(DetailView):
    model = Pengemudi
    template_name = 'pengemudi_detail.html'

class PemeriksaanCreate(CreateView):
    model = Pemeriksaan
    template_name = 'pemeriksaan_create.html'