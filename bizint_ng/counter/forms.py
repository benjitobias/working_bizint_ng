from django import forms


class CountForm(forms.Form):
    note = forms.CharField(label='Note', max_length=200, required=False)
    update_telegram = forms.BooleanField(label='Update Telegram?', required=False)


