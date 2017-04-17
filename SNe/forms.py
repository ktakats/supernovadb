from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, ObjectDoesNotExist
from  django.core.validators import RegexValidator
from django.db.models import Q

from .models import SN, Project

from astropy.coordinates import SkyCoord
from astropy import units as u
from collections import OrderedDict

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
        fields=['sn_name', 'sntype', 'host', 'z']

        labels={
            'sn_name': 'SN',
            'sntype': 'Type',
            'z': 'z'
        }

        widgets={
            'z': forms.TextInput()
        }

        error_messages={
        'sn_name': {'required': 'You need to provide the name of the SN'},
        }


    def __init__(self, *args, **kwargs):
        super(NewSNForm, self).__init__(*args, **kwargs)
        #Rearranges the order of the
        dec = self.fields.pop('dec')
        ra =self.fields.pop('ra')
        items=self.fields.items()
        items.insert(1, ('ra',ra))
        items.insert(2, ('dec',dec))
        self.fields=OrderedDict(items)

    def save(self, pi):
        data=self.cleaned_data
        coords=SkyCoord(data['ra'], data['dec'], unit=(u.hourangle, u.deg))
        sn=SN(sn_name=data['sn_name'], ra=coords.ra.deg, dec=coords.dec.deg, pi=pi, sntype=data['sntype'], host=data['host'], z=data['z'])
        sn.save()
        return sn

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict={'sn_name': ['This SN is already registered']}
            self._update_errors(e)

class AddCoIForm(forms.models.ModelForm):
    coinvestigators=forms.ModelChoiceField(queryset=None)

    class Meta:
        model=SN
        fields=["coinvestigators"]

        labels={
            'coinvestigators': "Co-Is"
        }


    def __init__(self, *args, **kwargs):
        super(AddCoIForm, self).__init__(*args, **kwargs)
        cois=[coi.id for coi in self.instance.coinvestigators.all()]
        try:
            pi=self.instance.pi.id
        except ObjectDoesNotExist:
            pi=None
        cois.append(pi)
        self.fields['coinvestigators'].queryset=Users.objects.exclude(id__in=cois)

class NewProjectForm(forms.models.ModelForm):
    coinvestigators=forms.ModelMultipleChoiceField(queryset=None, required=False)
    sne=forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model=Project
        fields=["title", "description", "coinvestigators", "sne"]
        error_messages={
            'title': {'required': "Give a title to your project"}
        }
        labels={
            'coinvestigators': 'Co-Is',
            'sne': 'SNe',
        }
        widgets={
            'description': forms.Textarea(attrs={
                "rows": "4",
                "cols": "25"
            })
        }

    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        try:
            pi=self.instance.id
        except ObjectDoesNotExist:
            pi=None
        self.fields['coinvestigators'].queryset=Users.objects.exclude(id=pi)
        self.fields['sne'].queryset=SN.objects.filter(Q(pi=pi) | Q(coinvestigators=pi))

    def save(self):
        data=self.cleaned_data
        project=Project.objects.create(title=data['title'], description=data['description'], pi=self.instance)
        for sn in data['sne']:
            #add sne to project
            project.sne.add(sn)
            #add project co-is (and if necessary project pi) as cois of the SN
            snpi=sn.pi
            sncois=sn.coinvestigators.all()
            if not self.instance==snpi or self.instance not in sncois:
                sn.coinvestigators.add(self.instance)
            for coi in data['coinvestigators']:
                if not coi==snpi or coi not in sncois:
                    sn.coinvestigators.add(coi)
            sn.save()
        #add Cois to the project
        for coi in data['coinvestigators']:
            project.coinvestigators.add(coi)
        project.save()
        return project
