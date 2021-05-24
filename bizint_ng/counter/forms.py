from django import forms


class CountForm(forms.Form):
    note = forms.CharField(label='Note', max_length=200, required=False)
    update_telegram = forms.BooleanField(label='Update Telegram?', required=False)
    longitude = forms.FloatField(label='longitude', widget=forms.HiddenInput(), initial=0)
    latitude = forms.FloatField(label='latitude', widget=forms.HiddenInput(), initial=0)
    ignore_location = forms.BooleanField(label='Ignore location?', required=False, widget=forms.CheckboxInput(attrs={'onclick': 'updatePosition();'}))
