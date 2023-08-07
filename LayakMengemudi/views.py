from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView, View
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
#from django.utils import timezone
import xlwt, xlrd
from django.http import HttpResponse
import pytz

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
        #q = "SELECT *, cast(round((julianday('now') - julianday(tanggal_lahir)) / 365) as int) as usia FROM LayakMengemudi_pengemudi"
        today = datetime.now().date()
        q = "SELECT *, FLOOR(DATEDIFF(CURDATE(), tanggal_lahir) / 365) as usia FROM LayakMengemudi_pengemudi"
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

#fungsi queryset untuk report pemeriksaan harian dan export datanya ke xls
def filter_pemeriksaan_queryset(request):
    queryset = Pemeriksaan.objects.all()
    daritanggal = request.GET.get('fromDate')
    sampaitanggal = request.GET.get('toDate')

    if daritanggal and sampaitanggal:
        daritanggal = datetime.strptime(daritanggal, '%Y-%m-%d')
        sampaitanggal = datetime.strptime(sampaitanggal, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    else:
        daritanggal = datetime.now().date()
        sampaitanggal = datetime.now().date() + timedelta(days=1)

    return queryset.filter(tanggal__range=(daritanggal, sampaitanggal)).order_by('tanggal')


class ReportPemeriksaanHarian(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Pemeriksaan
    template_name = 'report_pemeriksaan_harian.html'

    def get_queryset(self):
        return filter_pemeriksaan_queryset(self.request)

    '''def get_queryset(self):
        queryset = super().get_queryset()
        daritanggal = self.request.GET.get('fromDate') #datetime(2023, 6, 30, 0, 0, 0)#datetime.now().date()#datetime.date.today()
        sampaitanggal = self.request.GET.get('toDate') #datetime(2023, 6, 30, 23, 59, 59)
        if daritanggal and sampaitanggal:
            daritanggal = datetime.strptime(daritanggal, '%Y-%m-%d')
            sampaitanggal = datetime.strptime(sampaitanggal, '%Y-%m-%d').replace(hour=23, minute=59, second=59) #jika tidak pakai replace maka jamnya 0:0:0 dan input setelah itu dianggap beda hari
            #queryset = queryset.filter(tanggal__range=(daritanggal, sampaitanggal))
        else:
            daritanggal = datetime.now().date()
            sampaitanggal = datetime.now().date() + timedelta(days=1)

        queryset = queryset.filter(tanggal__range=(daritanggal, sampaitanggal)).order_by('tanggal')
        return queryset #Pemeriksaan.objects.filter(Q(tanggal__gte = daritanggal) & Q(tanggal__lte = sampaitanggal)).order_by('tanggal')'''
    #Pemeriksaan.objects.filter(tanggal__range = (daritanggal, sampaitanggal)).order_by('tanggal')  #Pemeriksaan.objects.filter(tanggal__date = daritanggal)#

    #untuk kirim parameter query ke export xls
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fromDate'] = self.request.GET.get('fromDate', '')
        context['toDate'] = self.request.GET.get('toDate', '')
        return context
    
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'dashboard.html'

class ExportToXLSView(View):
    def get(self, request, *args, **kwargs):
        #report_view = ReportPemeriksaanHarian()

        queryset = filter_pemeriksaan_queryset(request) #report_view.get_queryset() #Pemeriksaan.objects.all()
        timezone = pytz.timezone('Asia/Jakarta')

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Sheet1')

        # Convert to naive datetime, fix error saat export
        daritanggal = datetime.strptime(request.GET.get('fromDate'), '%Y-%m-%d')
        sampaitanggal = datetime.strptime(request.GET.get('toDate'), '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        # Create a style for the header cells
        header_style = xlwt.XFStyle()
        header_font = xlwt.Font()
        header_font.bold = True
        header_style.font = header_font

        headers = ['Tanggal', 'Pengemudi', 'Sistolik', 'Diastolik', 'Suhu', 'Jam Tidur', 'Gula Darah', 'Kolesterol', 'Alkohol', 'NAPZA', 'Kondisi', 'Fit/Tidak Fit']
        DBfield = ['tanggal', 'pengemudi', 'sistolik', 'diastolik', 'suhu', 'jam_tidur', 'gula_darah', 'kolesterol', 'alkohol', 'napza', 'kondisi', 'pengemudi.status' ]
        for col, header in enumerate(DBfield):
            worksheet.write(0, col, header, header_style)

            header_width = len(header) * 256  # Width is measured in 1/256 of the character width
            #data_width = max(len(str(item.__dict__[header])) for item in queryset) * 256
            #column_width = max(header_width, data_width) + 100  # Add some extra padding

            #worksheet.col(col).width = column_width

        for row, item in enumerate(queryset, start=1):
            item_tanggal_naive = item.tanggal.astimezone(timezone).replace(tzinfo=None)

            #base_date = datetime(1899, 12, 30)  # Excel base date is December 30, 1899
            #excel_date_delta = timedelta(days=item_tanggal_naive)
            #result_datetime = base_date + excel_date_delta

            result_datetime = xlrd.xldate_as_datetime(item_tanggal_naive, 0)  # 0 means the datemode is 1900-based
            item_tanggal_naive = result_datetime.strftime('%Y-%m-%d %H:%M:%S')

            data = [item_tanggal_naive, item.pengemudi.nama, item.sistolik, item.diastolik, item.suhu, item.jam_tidur, item.gula_darah, item.kolesterol, item.alkohol, item.napza, item.kondisi, item.pengemudi.status]
            for col, value in enumerate(data):
                if value == 'L' :
                    value = 'Fit Mengemudi'
                elif value == 'TL':
                    value = 'Tidak Fit Mengemudi'
                worksheet.write(row, col, value)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="export.xls"'
        workbook.save(response)
        return response