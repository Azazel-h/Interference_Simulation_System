from django.shortcuts import render
import plotly.express as px
from LightPipes import *

from .forms import GraphForm
from .models import RequestM, PresetM

import math
from django import forms


def index_page(request) -> render:
    context = {}
    form = GraphForm()

    if request.method == 'POST':
        if 'send_request' in request.POST or 'save_preset' in request.POST:
            form = GraphForm(request.POST)
            if form.is_valid():
                form_dict = dict(form.cleaned_data)
                form_dict['user'] = request.user

                if 'send_request' in request.POST:
                    RequestM.objects.create(**form_dict)
                    graph = get_graph(form_dict)
                    context['graph'] = graph

                elif 'save_preset' in request.POST:
                    presets = PresetM.objects.filter(user=request.user.username)[::-1]
                    if request.user.username and len(presets) < 5:
                        PresetM.objects.create(**form_dict)

        elif 'delete_preset' in request.POST:
            PresetM.objects.get(id=request.POST['delete_preset']).delete()

    presets = PresetM.objects.filter(user=request.user.username)[::-1]
    user_requests = RequestM.objects.filter(user=request.user.username)[::-1]
    context['presets'] = presets
    context['array_of_reqs'] = user_requests[:5]
    context['form'] = form

    return render(request, 'pages/michelson.html', context=context)


def get_graph(form_dict):
    R = 3 * mm
    z3 = 3 * cm
    z4 = 5 * cm
    wavelength = form_dict['wavelength'] * nm
    z1 = form_dict['z1'] * cm
    z2 = form_dict['z2'] * cm
    Rbs = form_dict['Rbs']
    tx = form_dict['tx'] * mrad
    ty = form_dict['ty'] * mrad
    f = form_dict['f'] * cm
    size = form_dict['size'] * mm
    N = form_dict['N']

    # img=mpimg.imread('Michelson.png')
    # plt.imshow(img); plt.axis('off')
    # plt.show()

    # Generate a weak converging laser beam using a weak positive lens:
    F = Begin(size, wavelength, N)
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

    # color_scale = [(0, 'purple'), (0.13, 'blue'), (0.23, 'aqua'), (0.35, 'lime'),
    #              (0.55, 'yellow'), (0.7, 'red'), (0.9, 'red'), (1, 'maroon')]
    # fig = px.axis('off')
    # fig = px.title('intensity pattern')
    config = {'displaylogo': False,'toImageButtonOptions': {'height': None, 'width': None}}
    fig = px.imshow(I)
    fig.update_yaxes(fixedrange=True)

    # print(px.colors.sequential.Inferno)
    graph = fig.to_html(full_html=False, config = config)
    return graph
