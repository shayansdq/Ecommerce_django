from django import forms
from django.utils.translation import gettext_lazy as _


class SubmitOrderForm(forms.Form):
    address = forms.CharField(label=_('Address'), widget=forms.Select(attrs={'class':'form-select'}))
    off_code = forms.CharField(max_length=12,label=_('Off Code'), widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

