from django import forms

from interferometers.widgets import RangeInput


class GraphForm(forms.Form):
    wavelength = forms.FloatField(
        label='Длина волны гелий-неонового лазера [нм]',
        min_value=200,
        max_value=800,
        initial=632.8,
        widget=RangeInput(min_value=200, max_value=800, step=0.1)
    )
    z1 = forms.FloatField(
        label='Длина первого плеча [см]',
        min_value=0,
        initial=8
    )
    z2 = forms.FloatField(
        label='Длина второго плеча [см]',
        min_value=0,
        initial=7
    )
    Rbs = forms.FloatField(
        label='Отражаемость разделитель луча',
        min_value=0,
        initial=0.5
    )
    tx = forms.FloatField(
        label='Наклон зеркала по X [мрад]',
        min_value=0,
        initial=1
    )
    ty = forms.FloatField(
        label='Наклон зеркала по Y [мрад]',
        min_value=0,
        initial=0
    )
    f = forms.FloatField(
        label='Фокусное расстояние положительной линзы [см]',
        min_value=0,
        initial=50
    )
    size = forms.FloatField(
        label='Размер рисунка [мм]',
        min_value=0,
        initial=10
    )
    N = forms.IntegerField(
        label='Разрешение',
        min_value=1,
        max_value=4000,
        initial=300
    )
