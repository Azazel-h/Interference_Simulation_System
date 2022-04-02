from django import forms

class GraphForm(forms.Form):
    DLABDA = forms.FloatField()
    NMEDIUM = forms.FloatField()
    labda = forms.FloatField(min_value=0.1)
    size = forms.FloatField()
    N = forms.IntegerField(min_value=1)
    D = forms.FloatField()
    R = forms.FloatField()
    f = forms.FloatField()
    k = forms.FloatField()