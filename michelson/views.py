from typing import Union

import plotly.express as px
import sepl_light_lib as sll
from LightPipes import *
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from .forms import GraphForm
from .models import RequestM, PresetM


# /michelson
def index_page(request) -> HttpResponse:
    context = {
        'presets': [],
        'array_of_reqs': [],
        'form': GraphForm()
    }

    if request.user.is_authenticated:
        context['presets'] = PresetM.objects.filter(user=request.user.username)[::-1]
        context['array_of_reqs'] = RequestM.objects.filter(user=request.user.username)[::-1][:5]

    return render(request, 'pages/michelson.html', context=context)


# /michelson/update_graph
def update_graph(request) -> Union[HttpResponse, None]:
    graph = None
    form = GraphForm(request.POST)

    if form.is_valid():
        form_dict = dict(form.cleaned_data)
        graph = get_graph(form_dict)

    return HttpResponse(graph)


# /michelson/update_history
def update_history(request) -> HttpResponse:
    context = {
        'array_of_reqs': []
    }
    form = GraphForm(request.POST)

    if request.user.is_authenticated and form.is_valid():
        form_dict = dict(form.cleaned_data)
        form_dict['user'] = request.user.username
        RequestM.objects.create(**form_dict)
        context['array_of_reqs'] = RequestM.objects.filter(user=request.user.username)[::-1][:5]

    return render(request, 'components/history-table-m.html', context=context)


# /michelson/update_preset
def update_preset(request) -> HttpResponse:
    context = {
        'presets': []
    }

    if request.user.is_authenticated:
        if request.POST.get('preset_operation') == 'save_preset':
            form = GraphForm(request.POST)

            if form.is_valid():
                form_dict = dict(form.cleaned_data)
                form_dict['user'] = request.user.username

                if len(PresetM.objects.filter(user=request.user.username)) < 5:
                    PresetM.objects.create(**form_dict)
        elif request.POST.get('preset_operation') == 'delete_preset':
            PresetM.objects.get(id=request.POST.get('delete_preset')).delete()

        context['presets'] = PresetM.objects.filter(user=request.user.username)[::-1]

    return render(request, 'components/presets-table-m.html', context=context)


def get_graph(form_dict) -> str:
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

    config = {'displaylogo': False, 'toImageButtonOptions': {'height': None, 'width': None}}

    return fig.to_html(config=config, include_plotlyjs=False, full_html=False)
