from django import forms

class GraphForm(forms.Form):
    wave_length = forms.FloatField(label='Длинна волны [nm]',min_value=0.1)
    glasses_distance = forms.FloatField(label='Расстояние между стеклами [mm]')
    focal_distance = forms.FloatField(label='Фокусное расстояние линзы [mm]')
    stroke_difference = forms.FloatField(label='Разница хода [nm]')
    reflectivity = forms.FloatField(label='Коэффициент отражения [--]')
    picture_size = forms.FloatField(label='Размер рисунка [mm]')
    N = forms.IntegerField(label='Разрешение', min_value=1)
    NMEDIUM = forms.FloatField(label='NMEDIUM')
