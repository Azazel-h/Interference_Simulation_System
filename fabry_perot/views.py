import math

import numpy as np
import plotly.express as px
import selph_light_lib as sll
from LightPipes import Begin, Intensity
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from misc.mixins.graph import GraphMixin
from misc.mixins.history import HistoryTableMixin
from misc.mixins.presets import PresetsTableMixin
from .forms import GraphForm
from .models import RequestFP, PresetFP

column_names = (
    "Длина волны",
    "Расстояние между стеклами",
    "Фокусное расстояние линзы",
    "Разница хода",
    "Коэффициент отражения",
    "Коэффициент преломления",
    "Размер рисунка",
    "Разрешение",
)


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
        wave_length_diff = form_dict['wave_length_diff'] * sll.nm
        reflection_coefficient = form_dict['reflection_coefficient']
        refractive_index = form_dict['refractive_index']
        picture_size = form_dict['picture_size'] * sll.mm
        resolution = form_dict['N']

        f = Begin(picture_size, wave_length, resolution)
        intensity = Intensity(f)
        wavenumber = 2 * math.pi / wave_length
        second_wavenumber = 2 * math.pi / (wave_length + wave_length_diff)
        fineness = 4.0 * reflection_coefficient / math.pow((1.0 - reflection_coefficient), 2)

        step = picture_size / resolution / sll.mm
        matrix_center = (resolution + 1) // 2

        for i in range(0, matrix_center):
            x_ray = (i + 0.5) * step
            for j in range(i, matrix_center):
                y_ray = (j + 0.5) * step

                x = x_ray * sll.mm - picture_size / 2
                y = y_ray * sll.mm - picture_size / 2

                radius = math.sqrt(x * x + y * y)
                theta = radius / focal_distance

                phase_diff = wavenumber * 2 * refractive_index * glasses_distance * math.cos(theta)
                light_intensity = 1 / (1 + fineness * math.pow(math.sin(phase_diff / 2), 2))

                phase_diff = second_wavenumber * 2 * refractive_index * glasses_distance * math.cos(theta)
                light_intensity += 1 / (1 + fineness * math.pow(math.sin(phase_diff / 2), 2))

                intensity[i][j] = intensity[j][i] = round(light_intensity, 6)


        intensity[resolution - matrix_center:resolution, 0:matrix_center] = np.rot90(intensity[0:matrix_center, 0:matrix_center])
        intensity[0:resolution, resolution - matrix_center:resolution] = np.rot90(intensity[0:resolution, 0:matrix_center], 2)
        intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))
        laser_color = sll.color.rgb_to_hex(sll.wave.wave_length_to_rgb(wave_length / sll.nm))
        fig = px.imshow(intensity, color_continuous_scale=['#000000', laser_color])
        fig.update_yaxes(fixedrange=True)

        config = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'height': None,
                'width': None
            }
        }

        return fig.to_html(config=config, include_plotlyjs=False, full_html=False)


# /fabry-perot/history
class HistoryTable(HistoryTableMixin):
    column_names = column_names
    form = GraphForm
    model = RequestFP


# /fabry-perot/preset
class PresetsTable(PresetsTableMixin):
    column_names = column_names
    model = PresetFP
    form = GraphForm
