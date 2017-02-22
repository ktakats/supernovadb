from django import forms
from .models import Photometry

class PhotometryForm(forms.models.ModelForm):

    class Meta:
        model=Photometry
        fields=['MJD', 'Filter', 'magnitude', 'mag_error', 'notes']

        widgets={
            'MJD': forms.fields.NumberInput(attrs={
                'placeholder': 'Modified Julian Date',
            }),
            'Filter': forms.fields.TextInput(attrs={
                'placeholder': 'One filter at the time, e.g. B',
            }),
            'magnitude': forms.fields.NumberInput(attrs={
                'placeholder': 'Mag',
            }),
            'mag_error': forms.fields.NumberInput(attrs={
                'placeholder': 'Mag error'
            }),
            'notes': forms.Textarea(attrs={
                'rows': "4",
                'cols': "25"
            })
        }

        labels={
            'mag_error': 'Error'
        }

    def save(self, sn, id=None):
        data=self.cleaned_data
        phot=Photometry(MJD=data['MJD'], Filter=data['Filter'], magnitude=data['magnitude'], mag_error=data['mag_error'], notes=data['notes'], sn=sn)
        if not id==None:
            phot.id=id
        phot.save()
        return phot

class UploadPhotometryFileForm(forms.Form):
    file=forms.FileField()
