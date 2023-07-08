import math

import numpy as np
import plotly.express as px
import sepl_light_lib as sll
from LightPipes import Begin, Intensity
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from misc.mixins.graph import GraphMixin
from misc.mixins.history import HistoryTableMixin
from misc.mixins.presets import PresetsTableMixin
from .forms import GraphForm
from .models import RequestFP, PresetFP


# /fabry-perot
class IndexPage(TemplateView):
    template_name = 'pages/fabry-perot.html'

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        context = {
            'form': GraphForm()
        }

        if request.user.is_authenticated:
            context['presets_table'] = PresetsTable.as_view()(request).rendered_content
            context['history_table'] = HistoryTable.as_view()(request).rendered_content

        return self.render_to_response(context)


# /fabry-perot/graph
class Graph(GraphMixin):
    form = GraphForm

    @staticmethod
    def get_graph(form_dict: dict) -> str:
        wave_length = form_dict['wave_length'] * sll.nm
        glasses_distance = form_dict['glasses_distance'] * sll.mm
        focal_distance = form_dict['focal_distance'] * sll.mm
        stroke_difference = form_dict['stroke_difference'] * sll.nm
        reflectivity = form_dict['reflectivity']
        refractive_index = form_dict['refractive_index']
        picture_size = form_dict['picture_size'] * sll.mm
        n = form_dict['N']

        f = Begin(picture_size, wave_length, n)
        intensity = Intensity(f)
        k = 2 * math.pi / wave_length
        second_k = 2 * math.pi / (wave_length + stroke_difference)
        fineness = 4.0 * reflectivity / (1.0 - reflectivity)

        step = picture_size / n / sll.mm
        matrix_center = (n + 1) // 2

        for i in range(0, matrix_center):
            x_ray = (i + 0.5) * step
            for j in range(i, matrix_center):
                y_ray = (j + 0.5) * step

                x = x_ray * sll.mm - picture_size / 2
                y = y_ray * sll.mm - picture_size / 2

                radius = math.sqrt(x * x + y * y)
                theta = radius / focal_distance

                delta = k * refractive_index * glasses_distance * math.cos(theta)
                light_intensity = 0.5 / (1 + fineness * math.pow(math.sin(delta), 2))
                delta = second_k * refractive_index * glasses_distance * math.cos(theta)
                light_intensity += 0.5 / (1 + fineness * math.pow(math.sin(delta), 2))

                intensity[i][j] = intensity[j][i] = round(light_intensity, 6)

        intensity[n - matrix_center:n, 0:matrix_center] = np.rot90(intensity[0:matrix_center, 0:matrix_center])
        intensity[0:n, n - matrix_center:n] = np.rot90(intensity[0:n, 0:matrix_center], 2)

        laser_color = sll.color.rgb_to_hex(sll.wave.wave_length_to_rgb(wave_length / sll.nm))
        fig = px.imshow(intensity, color_continuous_scale=['#000000', laser_color])
        fig.update_yaxes(fixedrange=True)

        config = {'displaylogo': False, 'toImageButtonOptions': {'height': None, 'width': None}}

        return fig.to_html(config=config, include_plotlyjs=False, full_html=False)


# /fabry-perot/history
class HistoryTable(HistoryTableMixin):
    model = RequestFP
    template_name = 'components/history-table.html'
    context_object_name = 'array_of_reqs'
    form = GraphForm


# /fabry-perot/preset
class PresetsTable(PresetsTableMixin):
    model = PresetFP
    template_name = 'components/presets-table.html'
    context_object_name = 'presets'
    form = GraphForm
