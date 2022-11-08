from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    template_name = 'components/slider.html'
