from django.urls import path
from .views import PengemudiCreate, PengemudiList, PengemudiDetail, PengemudiUpdate, Beranda
from . import views

urlpatterns = [
    path('', Beranda.as_view(), name='beranda'),
    path('pengemudi/create', PengemudiCreate.as_view(), name='pengemudi-create'),
    path('pengemudi/update/<int:pk>', PengemudiUpdate.as_view(), name='pengemudi-update'),
    path('pengemudi/update/', PengemudiUpdate.as_view(), name='pengemudi-update'),
    path('pengemudi/list', PengemudiList.as_view(), name='pengemudi-list'),
    path('pengemudi/<int:pk>/', PengemudiDetail.as_view(), name='pengemudi-detail'),
    ]