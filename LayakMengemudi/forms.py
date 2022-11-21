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

class FormPengemudiCreate(ModelForm):
    class Meta:
        model = Pengemudi
        fields = '__all__'
        exclude = ['status', 'periksa_terakhir']
        labels = {'pasfoto_path':'Pas Foto'}

        widgets = {
            'nama': forms.TextInput({'class':'form-control'}),
            'tanggal_lahir': forms.TextInput({'class':'form-control'}),
            'kota_kelahiran': forms.TextInput({'class':'form-control'}),
            'alamat': forms.TextInput({'class':'form-control'}),
            'nik' : forms.TextInput({'class':'form-control'}),
            'pool' : forms.TextInput({'class':'form-control'}),
            'bus': forms.TextInput({'class':'form-control'}),
            'pasfoto_path': forms.TextInput({'class':'form-control'}),
            'qrcode_path': forms.TextInput({'class':'form-control', 'type':'hidden'}),
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
            'pengemudi': forms.Select({'class': 'form-control form-select'}),
            'tanggal': forms.TextInput({'class': 'form-control datepicker', 'autocomplete': 'off',
                                        'value': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}),
            'tensi': forms.TextInput({'class': 'form-control', 'placeholder': '120/80'}),
            'suhu': forms.TextInput({'class': 'form-control', 'placeholder': '36.1'}),
            'jam_tidur': forms.TextInput({'class': 'form-control', 'placeholder': '8'}),
            'kondisi': forms.Textarea({'class': 'form-control'}),
            'status': forms.Select({'class': 'form-control form-select'}),
        }