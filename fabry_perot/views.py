import math

import numpy as np
import plotly.express as px
import selph_light_lib as sll
from LightPipes import Begin, Intensity
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from plotly.graph_objs import Figure

from misc.mixins.graph import GraphMixin
from misc.mixins.graph_report import GraphReportMixin
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


class Graph:
    form_dict = {}

    def __init__(self, form_dict):
        self.form_dict = form_dict

    def create_figure(self) -> Figure:
        wave_length = self.form_dict['wave_length'] * sll.nm
        glasses_distance = self.form_dict['glasses_distance'] * sll.mm
        focal_distance = self.form_dict['focal_distance'] * sll.mm
        stroke_difference = self.form_dict['stroke_difference'] * sll.nm
        reflectivity = self.form_dict['reflectivity']
        refractive_index = self.form_dict['refractive_index']
        picture_size = self.form_dict['picture_size'] * sll.mm
        n = self.form_dict['N']

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

        return fig


# /fabry-perot/graph
class ShowGraph(GraphMixin):
    form = GraphForm

    @staticmethod
    def get_graph(form_dict: dict) -> Figure:
        new_graph = Graph(form_dict=form_dict)
        return new_graph.create_figure()


# /fabry-perot/graph-report
class GraphReport(GraphReportMixin):
    form = GraphForm

    @staticmethod
    def get_graph(form_dict: dict) -> Figure:
        new_graph = Graph(form_dict=form_dict)
        return new_graph.create_figure()


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
