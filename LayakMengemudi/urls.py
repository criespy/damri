from django.urls import path
from .views import PengemudiCreate, PengemudiList, PengemudiDetail
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pengemudi/create', PengemudiCreate.as_view(), name='pengemudi-create'),
    path('pengemudi/list', PengemudiList.as_view(), name='pengemudi-list'),
    path('pengemudi/<int:pk>/', PengemudiDetail.as_view(), name='pengemudi-detail'),
    ]