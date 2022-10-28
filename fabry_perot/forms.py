from django import forms


class GraphForm(forms.Form):
    wave_length = forms.FloatField(label='Длина волны [нм]',
                                   min_value=380,
                                   max_value=780,
                                   initial=630)
    glasses_distance = forms.FloatField(label='Расстояние между стеклами [мм]',
                                        min_value=0,
                                        initial=15)
    focal_distance = forms.FloatField(label='Фокусное расстояние линзы [мм]',
                                      min_value=0,
                                      initial=100)
    stroke_difference = forms.FloatField(label='Разница хода [нм]',
                                         min_value=0,
                                         initial=0)
    reflectivity = forms.FloatField(label='Коэффициент отражения [--]',
                                    min_value=0,
                                    max_value=0.9999,
                                    initial=0.7)
    refractive_index = forms.FloatField(label='Коэффициент преломления',
                                        min_value=1,
                                        initial=1)
    picture_size = forms.FloatField(label='Размер рисунка [мм]',
                                    min_value=0,
                                    initial=5)
    incident_light_intensity = forms.FloatField(label='Значение интенсивности излучения лазера [W / (cm * cm)]',
                                                min_value=0,
                                                initial=1000)
    N = forms.IntegerField(label='Разрешение',
                           min_value=1,
                           initial=500)

