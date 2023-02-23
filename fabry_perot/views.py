import math
from typing import Optional

import numpy as np
import plotly.express as px
import sepl_light_lib as sll
from LightPipes import *
from django.http import HttpResponse
from django.shortcuts import render

from .forms import GraphForm
from .models import RequestFP, PresetFP


# /fabry_perot
def index_page(request) -> HttpResponse:
    context = {
        'presets': [],
        'array_of_reqs': [],
        'form': GraphForm()
    }

    if request.user.is_authenticated:
        context['presets'] = PresetFP.objects.filter(user=request.user.username)[::-1]
        context['array_of_reqs'] = RequestFP.objects.filter(user=request.user.username)[::-1][:5]

    return render(request, 'pages/fabry-perot.html', context=context)


# /fabry_perot/update_graph
def update_graph(request) -> Optional[HttpResponse]:
    graph = None
    form = GraphForm(request.POST)

    if form.is_valid():
        form_dict = dict(form.cleaned_data)
        graph = get_graph(form_dict)

    return HttpResponse(graph)


# /fabry_perot/update_history
def update_history(request) -> HttpResponse:
    context = {
        'array_of_reqs': []
    }
    form = GraphForm(request.POST)

    if request.user.is_authenticated and form.is_valid():
        form_dict = dict(form.cleaned_data)
        form_dict['user'] = request.user.username
        RequestFP.objects.create(**form_dict)
        context['array_of_reqs'] = RequestFP.objects.filter(user=request.user.username)[::-1][:5]

    return render(request, 'components/history-table.html', context=context)


# /fabry_perot/update_preset
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

                if len(PresetFP.objects.filter(user=request.user.username)) < 5:
                    PresetFP.objects.create(**form_dict)
        elif request.POST.get('preset_operation') == 'delete_preset':
            PresetFP.objects.get(id=request.POST.get('delete_preset')).delete()

        context['presets'] = PresetFP.objects.filter(user=request.user.username)[::-1]

    return render(request, 'components/presets-table.html', context=context)


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

    step = picture_size / n / mm
    matrix_center = (n + 1) // 2

    for i in range(0, matrix_center):
        x_ray = (i + 0.5) * step
        for j in range(i, matrix_center):
            y_ray = (j + 0.5) * step

            x = x_ray * mm - picture_size / 2
            y = y_ray * mm - picture_size / 2

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
