from astropy.coordinates import SkyCoord
from astropy import units as u

from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from  django.core.validators import RegexValidator
from django.contrib import auth

from .models import SN
Users=auth.get_user_model()

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

    def save(self, pi):
        data=self.cleaned_data
        coords=SkyCoord(data['ra'], data['dec'], unit=(u.hourangle, u.deg))
        sn=SN(sn_name=data['sn_name'], ra=coords.ra.deg, dec=coords.dec.deg, pi=pi)
        sn.save()
        return sn

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict={'sn_name': ['This SN is already registered']}
            self._update_errors(e)

class AddCoIForm(forms.models.ModelForm):
    coinvestigators=forms.ModelChoiceField(queryset=Users.objects.all())

    class Meta:
        model=SN
        fields=["coinvestigators"]

        labels={
            'coinvestigators': "Co-Is"
        }
