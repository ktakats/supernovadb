from astropy.coordinates import SkyCoord
from astropy import units as u

from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from  django.core.validators import RegexValidator

from .models import SN, Obs, Photometry

#from django.forms.extras.widgets import SelectDateWidget


def validate_ra(value):
    ra=map(float, value.split(":"))
    if ra[0]<0 or ra[0]>=24 or ra[1]>=60 or ra[2]>=60:
        raise ValidationError("Invalid coordinate value")

def validate_dec(value):
    dec=map(float, value.split(":"))
    if dec[0]>=90 or dec[0]<=-90 or dec[1]>=60 or dec[2]>=60:
        raise ValidationError("Invalid coordinate value")

class NewSNForm(forms.models.ModelForm):
    ra=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00:00:00.000'}),
        validators=[RegexValidator(regex='^(\+|-?)\d\d:\d\d:\d\d.\d(\d*?)$', message='Incorrect coordinate format'),
        validate_ra,])

    dec=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00:00:00.00'}),
        validators=[RegexValidator(regex='^(\+|-?)\d\d:\d\d:\d\d.\d(\d*?)$', message='Incorrect coordinate format'),
        validate_dec])


    class Meta:
        model=SN
        fields=['sn_name']

        labels={
            'sn_name': 'SN'
        }

        error_messages={
        'sn_name': {'required': 'You need to provide the name of the SN'},
        }

    def save(self):
        data=self.cleaned_data
        coords=SkyCoord(data['ra'], data['dec'], unit=(u.hourangle, u.deg))
        sn=SN(sn_name=data['sn_name'], ra=coords.ra.deg, dec=coords.dec.deg)
        sn.save()
        return sn

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict={'sn_name': ['This SN is already registered']}
            self._update_errors(e)


class ObsLogForm(forms.models.ModelForm):

    class Meta:
        model=Obs
        fields=['obs_date', 'obs_type', 'telescope', 'instrument', 'setup', 'notes']

        widgets={
            'obs_date': forms.widgets.DateInput(format='%Y-%m-%d', attrs={
                'placeholder': 'e.g. 2017-01-31'
            }),
            'setup': forms.fields.TextInput(attrs={
                'placeholder': 'e.g. filters, grisms',
                }),
        }

    def save(self, sn, id=None):
        data=self.cleaned_data
        obs=Obs(obs_date=data['obs_date'], obs_type=data['obs_type'], telescope=data['telescope'], instrument=data['instrument'], setup=data['setup'], notes=data['notes'], sn=sn)
        if not id==None:
            obs.id=id
        obs.save()
        return obs

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
