from django import forms
from django.forms import ModelForm
from LayakMengemudi.models import *
from datetime import date

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