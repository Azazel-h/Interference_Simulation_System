import math
from typing import Optional, Union

import numpy as np
import pandas as pd
import plotly.express as px
import selph_light_lib as sll
from LightPipes import Begin, Intensity
from django.apps import apps
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
    def get_graph(form_dict: dict) -> Optional[dict[str, Union[str, tuple[str, ...]]]]:
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

        theta_array = []
        first_beam = []
        second_beam = []
        for i in range(0, matrix_center):
            x_ray = (i + 0.5) * step
            for j in range(i, matrix_center):
                y_ray = (j + 0.5) * step

                x = x_ray * sll.mm - picture_size / 2
                y = y_ray * sll.mm - picture_size / 2
                radius = math.sqrt(x * x + y * y)

                theta = math.atan2(radius, focal_distance)

                phase_diff = wavenumber * 2 * refractive_index * glasses_distance * math.cos(theta)
                first_light_intensity = 1 / (1 + fineness * math.pow(math.sin(phase_diff / 2), 2))

                phase_diff = second_wavenumber * 2 * refractive_index * glasses_distance * math.cos(theta)
                second_light_intensity = first_light_intensity + (
                        1 / (1 + fineness * math.pow(math.sin(phase_diff / 2), 2)))

                intensity[i][j] = intensity[j][i] = second_light_intensity

                if i == j:
                    first_beam.append(first_light_intensity)
                    second_beam.append(second_light_intensity)
                    theta_array.append(theta)

        # TODO: Вывести все это в интерфейс
        dispersion_region = math.pow(wave_length + wave_length_diff, 2) / (2 * glasses_distance)

        # print(theta_array, first_beam, second_beam)

        intensity[resolution - matrix_center:resolution, 0:matrix_center] = np.rot90(
            intensity[0:matrix_center, 0:matrix_center])
        intensity[0:resolution, resolution - matrix_center:resolution] = np.rot90(
            intensity[0:resolution, 0:matrix_center], 2)
        intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

        laser_color = sll.color.rgb_to_hex(sll.wave.wave_length_to_rgb(wave_length / sll.nm))

        fig_1 = px.imshow(intensity, color_continuous_scale=['#000000', laser_color])
        fig_1.update_yaxes(fixedrange=True)

        df = pd.DataFrame(
            dict(
                x=theta_array,
                y=second_beam,
                color=laser_color
            )
        )

        fig_2 = px.line(df, x="x", y="y", labels={'y': 'Интенсивность', 'x': 'Угол падения'})
        fig_2.update_traces(line_color=laser_color)
        fig_2.update_layout(
            plot_bgcolor='white'
        )
        fig_2.update_xaxes(
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig_2.update_yaxes(
            linecolor='black',
            gridcolor='lightgrey',
        )

        config = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'height': None,
                'width': None
            }
        }

        return {
            'graph': (
                fig_1.to_html(config=config, include_plotlyjs=False, full_html=False),
                fig_2.to_html(config=config, include_plotlyjs=False, full_html=False),
            ),
            'additional': f'<span>Область дисперсии: {dispersion_region}</span>'
        }


# /fabry-perot/history
class HistoryTable(HistoryTableMixin):
    column_names = apps.get_app_config('fabry_perot').column_names
    form = GraphForm
    model = RequestFP


# /fabry-perot/preset
class PresetsTable(PresetsTableMixin):
    column_names = apps.get_app_config('fabry_perot').column_names
    model = PresetFP
    form = GraphForm
