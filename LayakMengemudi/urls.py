from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Beranda.as_view(), name='beranda'),
    path('pengemudi/create', PengemudiCreate.as_view(), name='pengemudi-create'),
    path('pengemudi/update/<int:pk>', PengemudiUpdate.as_view(), name='pengemudi-update'),
    path('pengemudi/update/', PengemudiUpdate.as_view(), name='pengemudi-update'),
    path('pengemudi/list', PengemudiList.as_view(), name='pengemudi-list'),
    #path('pengemudi/<int:pk>/', PengemudiDetail.as_view(), name='pengemudi-detail'),
    path('pengemudi/<slug:slug>', PengemudiDetail.as_view(), name='pengemudi-detail'),
    path('pemeriksaan/create/', PemeriksaanCreate.as_view(), name='pemeriksaan-create'),
    path('pemeriksaan/create/<int:pk>', PemeriksaanCreate.as_view(), name='pemeriksaan-create'),
    path('pengemudi/print_id/', PrintIDCard.as_view(), name='print-id'),
    path('pengemudi/print_id/<slug:slug>', PrintIDCard.as_view(), name='print-id'),
    path('report/', ReportView.as_view(), name='report'),
    path('report/pemeriksaan-harian', ReportPemeriksaanHarian.as_view(), name='report_pemeriksaan_harian'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('export-xls/', ExportToXLSView.as_view(), name='export_to_xls'),
    ]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)