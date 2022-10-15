from django import forms


class GraphForm(forms.Form):
    wavelength = forms.FloatField(label='длина волны гелий-неонового лазера [нм]', min_value=200, max_value=800)
    R = forms.FloatField(label='радиус лазерного луча [мм]', min_value=0)
    z1 = forms.FloatField(label='Длина первого плеча [см]', min_value=0)
    z2 = forms.FloatField(label='Длина второго плеча [см]', min_value=0)
    z3 = forms.FloatField(label='расстояние от лазера до разделителя луча [см]', min_value=0)
    z4 = forms.FloatField(label='расстояние от разделителя до экрана [см]', min_value=0)
    Rbs = forms.FloatField(label='Отражаемость разделитель луча', min_value=0)
    tx = forms.FloatField(label='Наклон зеркала по X [мрад]', min_value=0)
    ty = forms.FloatField(label='Наклон зеркала по Y [мрад]', min_value=0)
    f = forms.FloatField(label='фокусное расстояние положительной линзы [см]', min_value=0)
    size = forms.FloatField(label='Размер рисунка [мм]', min_value=0)
    N = forms.IntegerField(label='Разрешение', min_value=1)
