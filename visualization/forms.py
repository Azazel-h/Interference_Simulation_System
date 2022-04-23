from django import forms

class GraphForm(forms.Form):
    laser_color = forms.ChoiceField(label='Цвет лазера', choices=(('g', 'Зеленый - 532 нм'), ('r', 'Красный - 630 нм')))
    glasses_distance = forms.FloatField(label='Расстояние между стеклами [мм]', min_value=0)
    focal_distance = forms.FloatField(label='Фокусное расстояние линзы [мм]', min_value=0)
    stroke_difference = forms.FloatField(label='Разница хода [нм]', min_value=0)
    reflectivity = forms.FloatField(label='Коэффициент отражения [--]', min_value=0, max_value=0.9999)
    refractive_index = forms.FloatField(label='Коэффициент преломления', min_value=1)
    picture_size = forms.FloatField(label='Размер рисунка [мм]', min_value=0)
    N = forms.IntegerField(label='Разрешение', min_value=1)
