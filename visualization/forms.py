from django import forms

class GraphForm(forms.Form):
    wave_length = forms.FloatField(label='Wave Length [nm]',min_value=0.1)
    glasses_distance = forms.FloatField(label='Glasses Distance [mm]')
    focal_distance = forms.FloatField(label='Focal Distance [mm]')
    stroke_difference = forms.FloatField(label='Stroke Difference [nm]')
    reflectivity = forms.FloatField(label='Reflectivity [--]')
    picture_size = forms.FloatField(label='Picture Size [mm]')
    N = forms.IntegerField(label='Resolution', min_value=1)
    NMEDIUM = forms.FloatField(label='NMEDIUM')
