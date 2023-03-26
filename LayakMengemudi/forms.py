from django import forms
from django.forms import ModelForm, fields, widgets, formset_factory
from django.forms.models import inlineformset_factory
from LayakMengemudi.models import *
from datetime import date

FormSetUpdatePengemudi = inlineformset_factory(Pengemudi, Pemeriksaan, fields=('__all__'), extra=1, can_delete=False, widgets={
        'pengemudi': forms.TextInput({'class':'form-control form-select'}),
        'tanggal' : forms.TextInput({'class':'form-control datepicker','autocomplete':'off', 'value':datetime.now().strftime("%Y-%m-%d %H:%M:%S")}),
        'tensi' : forms.TextInput({'class':'form-control','placeholder':'120/80'}),
        'suhu' : forms.TextInput({'class':'form-control', 'placeholder':'36.1'}),
        'jam_tidur' : forms.TextInput({'class':'form-control', 'placeholder':'8'}),
        'kondisi' : forms.Textarea({'class':'form-control'})
        })

#form yang digunakan untuk menampilkan hasil pemeriksaan terakhir
FormPemeriksaanTerakhir = inlineformset_factory(Pengemudi, Pemeriksaan, fields=(['sistolik', 'diastolik', 'suhu', 'jam_tidur', 'gula_darah', 'kolesterol', 'alkohol', 'kondisi']), extra=1, can_delete=False, widgets={
        'sistolik' : forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'diastolik' : forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'suhu' : forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'jam_tidur' : forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'gula_darah': forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'kolesterol': forms.TextInput({'class':'form-control', 'disabled':'disabled'}),
        'alkohol': forms.TextInput({'class': 'form-control', 'disabled':'disabled'}),
        'kondisi' : forms.Textarea({'class':'form-control', 'disabled':'disabled'})
        })

class FormPengemudiCreate(ModelForm):
    class Meta:
        model = Pengemudi
        fields = '__all__'
        exclude = ['status', 'periksa_terakhir']
        labels = {'nomor_hp':'Nomor HP', 'qrcode_path':''}
        help_texts = {
            'tanggal_lahir': '<span class="my-class" id="usia">Usia: </span>',
        }

        widgets = {
            'nama': forms.TextInput({'class':'form-control'}),
            'tanggal_lahir': forms.TextInput({'class':'form-control'}),
            'kota_kelahiran': forms.TextInput({'class':'form-control'}),
            'alamat': forms.TextInput({'class':'form-control'}),
            'nik' : forms.TextInput({'class':'form-control', 'id':'nik'}),
            'nomor_hp' : forms.TextInput({'class':'form-control'}),
            'email' : forms.EmailInput({'class':'form-control'}),
            'pendidikan_terakhir' : forms.TextInput({'class':'form-control'}),
            'pool' : forms.TextInput({'class':'form-control'}),
            'bus': forms.TextInput({'class':'form-control'}),
            'pasfoto': forms.FileInput({'class':'form-control'}),
            'qrcode_path': forms.TextInput({'class':'form-control', 'id':'qrpath', 'hidden':'hidden'}),
        }

#class FormPemeriksaanCreate(ModelForm):
#    class Meta:
#        model = Pengemudi
#        fields = ['nama', 'status', 'periksa_terakhir']
#        labels = {'suhu':'Suhu (°C)', 'jam_tidur':'Jumlah Jam Tidur', 'tensi':'Tensi (mmHg)'}
#        icons = {'tensi':'fa fa-user'}
#
#        widgets = {
#            'nama': forms.TextInput({'class':'form-control'}),
#            'status': forms.Select({'class':'form-control form-select'}),
#            'periksa_terakhir': forms.TextInput({'class':'form-control', 'hidden':'true' }),
#        }

class FormPemeriksaanCreate(ModelForm):
    class Meta:
        model = Pemeriksaan
        fields = '__all__'
        widgets = {
            'pengemudi': forms.Select({'class': 'form-control form-select select2'}),
            'tanggal': forms.TextInput({'class': 'form-control datepicker', 'autocomplete': 'off', 'value': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}),
            'sistolik': forms.NumberInput({'class': 'form-control'}),
            'diastolik': forms.NumberInput({'class': 'form-control'}),
            'suhu': forms.TextInput({'class': 'form-control', 'placeholder': '36.1'}),
            'jam_tidur': forms.TextInput({'class': 'form-control', 'placeholder': '8'}),
            'gula_darah': forms.TextInput({'class':'form-control'}),
            'kolesterol': forms.TextInput({'class':'form-control'}),
            'alkohol': forms.NumberInput({'class': 'form-control'}),
            'napza': forms.Select({'class': 'form-control form-select'}),
            'kondisi': forms.Textarea({'class': 'form-control'}),
            'status': forms.Select({'class': 'form-control form-select'}),
        }