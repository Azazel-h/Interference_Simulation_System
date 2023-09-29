from django.forms.widgets import TextInput


class RangeInput(TextInput):
    input_type = 'range'
    template_name = 'components/slider.html'

    def __init__(self, min_value, max_value, step):
        super().__init__()
        self.attrs = {
            'min': min_value,
            'max': max_value,
            'step': step
        }
