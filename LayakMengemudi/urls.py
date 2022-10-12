from django.urls import path
from .views import PengemudiDetail
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pengemudi/<int:pk>/', PengemudiDetail.as_view(), name='pengemudi-detail')
    ]