from django import forms

class GraphForm(forms.Form):
    DLABDA = forms.FloatField()
    NMEDIUM = forms.FloatField()
    labda = forms.FloatField()
    size = forms.FloatField()
    N = forms.IntegerField()
    D = forms.FloatField()
    R = forms.FloatField()
    f = forms.FloatField()
    k = forms.FloatField()