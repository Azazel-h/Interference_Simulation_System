from typing import Optional, Union

import plotly.express as px
import selph_light_lib as sll
from LightPipes import *
from django.apps import apps
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from misc.mixins.graph import GraphMixin
from misc.mixins.history import HistoryTableMixin
from misc.mixins.presets import PresetsTableMixin
from .forms import GraphForm
from .models import RequestM, PresetM


# /michelson
class IndexPage(TemplateView):
    template_name = 'pages/michelson.html'

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        context = {
            'form': GraphForm()
        }

        if request.user.is_authenticated:
            context['presets_table'] = PresetsTable.as_view()(request).rendered_content
            context['history_table'] = HistoryTable.as_view()(request).rendered_content

        return self.render_to_response(context)


# /michelson/graph
class Graph(GraphMixin):
    form = GraphForm

    @staticmethod
    def get_graph(form_dict: dict) -> Optional[dict[str, Union[str, tuple[str, ...]]]]:
        R = 3 * sll.mm
        z3 = 3 * sll.cm
        z4 = 5 * sll.cm
        wave_length = form_dict['wave_length'] * sll.nm
        z1 = form_dict['z1'] * cm
        z2 = form_dict['z2'] * cm
        Rbs = form_dict['Rbs']
        tx = form_dict['tx'] * sll.mrad
        ty = form_dict['ty'] * sll.mrad
        f = form_dict['f'] * sll.cm
        picture_size = form_dict['picture_size'] * sll.mm
        N = form_dict['N']

        # img=mpimg.imread('Michelson.png')
        # plt.imshow(img); plt.axis('off')
        # plt.show()

        # Generate a weak converging laser beam using a weak positive lens:
        F = Begin(picture_size, wave_length, N)
        # F=GaussBeam(F, R)
        # F=GaussHermite(F,R,0,0,1) #new style
        F = GaussHermite(F, R)  # new style
        # F=GaussHermite(0,0,1,R,F) #old style
        F = Lens(f, 0, 0, F)

        # Propagate to the beamsplitter:
        F = Forvard(z3, F)

        # Split the beam and propagate to mirror #2:
        F2 = IntAttenuator(1 - Rbs, F)
        F2 = Forvard(z2, F2)

        # Introduce tilt and propagate back to the beamsplitter:
        F2 = Tilt(tx, ty, F2)
        F2 = Forvard(z2, F2)
        F2 = IntAttenuator(Rbs, F2)

        # Split off the second beam and propagate to- and back from the mirror #1:
        F10 = IntAttenuator(Rbs, F)
        F1 = Forvard(z1 * 2, F10)
        F1 = IntAttenuator(1 - Rbs, F1)

        # Recombine the two beams and propagate to the screen:
        F = BeamMix(F1, F2)
        F = Forvard(z4, F)
        I = Intensity(1, F)

        laser_color = sll.color.rgb_to_hex(sll.wave.wave_length_to_rgb(wave_length / sll.nm))
        fig = px.imshow(I, color_continuous_scale=['#000000', laser_color])
        fig.update_yaxes(fixedrange=True)

        config = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'height': None,
                'width': None
            }
        }

        return {
            "graph": fig.to_html(config=config, include_plotlyjs=False, full_html=False)
        }


# /michelson/history
class HistoryTable(HistoryTableMixin):
    column_names = apps.get_app_config('michelson').column_names
    model = RequestM
    form = GraphForm


# /michelson/preset
class PresetsTable(PresetsTableMixin):
    column_names = apps.get_app_config('michelson').column_names
    model = PresetM
    form = GraphForm
