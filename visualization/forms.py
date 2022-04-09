from django import forms

class GraphForm(forms.Form):
    wave_length = forms.FloatField(label='Длинна волны [nm]', min_value=0.1)
    glasses_distance = forms.FloatField(label='Расстояние между стеклами [mm]', min_value=0)
    focal_distance = forms.FloatField(label='Фокусное расстояние линзы [mm]', min_value=0)
    stroke_difference = forms.FloatField(label='Разница хода [nm]', min_value=0)
    reflectivity = forms.FloatField(label='Коэффициент отражения [--]', min_value=0, max_value=1)
    picture_size = forms.FloatField(label='Размер рисунка [mm]', min_value=0)
    N = forms.IntegerField(label='Разрешение', min_value=1)
    NMEDIUM = forms.FloatField(label='Коэфицент (NMEDIUM)', min_value=0)
