from astropy.coordinates import SkyCoord
from astropy import units as u

from django import forms
from  django.core.validators import RegexValidator

from .models import SN

class NewSNForm(forms.models.ModelForm):
    ra=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00:00:00.00'}),
        validators=[RegexValidator(regex='^(\+|-?)\d\d:\d\d:\d\d.\d(\d*?)$', message='Incorrect coordinate format'),])
    dec=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00:00:00.00'}),
        validators=[RegexValidator(regex='^(\+|-?)\d\d:\d\d:\d\d.\d(\d*?)$', message='Incorrect coordinate format'),])


    class Meta:
        model=SN
        fields=['sn_name']

        error_messages={
        'sn_name': {'required': 'You need to provide the name of the SN'}
        }

    def save(self):
        data=self.cleaned_data
        coords=SkyCoord(data['ra'], data['dec'], unit=(u.hourangle, u.deg))
        sn=SN(sn_name=data['sn_name'], ra=coords.ra.deg, dec=coords.dec.deg)
        sn.save()
        return sn
