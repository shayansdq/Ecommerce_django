from django import forms


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mr-sm-2",'type':'search"',
                                                           'placeholder':'Search','aria-label':'Search'}))
