from django import forms

from misc.interface.widgets import RangeInput


class GraphForm(forms.Form):
    wave_length = forms.FloatField(
        label='Длина волны \\(\\lambda\\) [нм]',
        min_value=380,
        max_value=780,
        step_size=0.1,
        initial=630,
        widget=RangeInput(min_value=380, max_value=780, step=0.1)
    )
    wave_length_diff = forms.FloatField(
        label='Разница длин волн \\(\\Delta\\lambda\\) [нм]',
        min_value=0,
        step_size=0.000001,
        initial=0
    )
    glasses_distance = forms.FloatField(
        label='Расстояние между зеркалами \\(d\\) [мм]',
        min_value=0,
        step_size=0.001,
        initial=15,
    )
    focal_distance = forms.FloatField(label='Фокусное расстояние линзы \\(f\\) [мм]', min_value=0, step_size=0.001, initial=100)
    reflection_coefficient = forms.FloatField(
        label='Коэффициент отражения \\(R\\)',
        min_value=0.000001,
        max_value=0.999999,
        step_size=0.000001,
        initial=0.7,
        widget=RangeInput(min_value=0.000001, max_value=0.999999, step=0.000001)
    )
    refractive_index = forms.FloatField(label='Показатель преломления \\(n\\)', min_value=1, step_size=0.000001, initial=1)
    picture_size = forms.FloatField(label='Размер рисунка [мм]', min_value=0, step_size=0.001, initial=5)
    N = forms.IntegerField(label='Разрешение на экране в пикселях', min_value=1, max_value=1000, initial=500)
