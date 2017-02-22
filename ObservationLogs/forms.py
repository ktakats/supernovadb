from django import forms
from ObservationLogs.models import Obs

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
