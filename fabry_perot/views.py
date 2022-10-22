import math

import plotly.express as px
from LightPipes import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import RequestFP, PresetFP

from .forms import GraphForm


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
                    RequestFP.objects.create(**form_dict)
                    graph = get_graph(form_dict)
                    context['graph'] = graph

                elif 'save_preset' in request.POST:
                    presets = PresetFP.objects.filter(user=request.user.username)[::-1]
                    if request.user.username and len(presets) < 5:
                        PresetFP.objects.create(**form_dict)

        elif 'delete_preset' in request.POST:
            PresetFP.objects.get(id=request.POST['delete_preset']).delete()

    presets = PresetFP.objects.filter(user=request.user.username)[::-1]
    user_requests = RequestFP.objects.filter(user=request.user.username)[::-1]
    context['presets'] = presets
    context['array_of_reqs'] = user_requests[:5]
    context['form'] = form

    return render(request, 'pages/fabry-perot.html', context=context)


def get_graph(form_dict):

    picture_size = form_dict['picture_size'] * mm
    focal_distance = form_dict['focal_distance'] * mm
    glasses_distance = form_dict['glasses_distance'] * mm
    stroke_difference = form_dict['stroke_difference'] * nm
    reflectivity = form_dict['reflectivity']
    refractive_index = form_dict['refractive_index']
    incident_light_intensity = form_dict['incident_light_intensity'] * W / cm / cm
    laser_color = form_dict['laser_color']

    if laser_color == 'g':
        wave_length = 532 * nm
    else:
        wave_length = 630 * nm

    n = form_dict['N']

    f = Begin(picture_size, wave_length, n)
    intensity = Intensity(f, 1)

    k = 2 * math.pi / wave_length
    second_k = 2 * math.pi / (wave_length + stroke_difference)
    fineness = 4.0 * reflectivity / math.pow(1.0 - reflectivity, 2)

    step = picture_size / n / mm
    for i in range(1, n):
        x_ray = i * step
        for j in range(1, n):
            y_ray = j * step

            x = x_ray * mm - picture_size / 2
            y = y_ray * mm - picture_size / 2

            radius = math.sqrt(x * x + y * y)
            theta = radius / focal_distance

            delta = 2 * k * refractive_index * glasses_distance * math.cos(theta)
            light_intensity = incident_light_intensity / (1 + fineness * math.pow(math.sin(delta / 2), 2))
            delta = 2 * second_k * refractive_index * glasses_distance * math.cos(theta)
            light_intensity += incident_light_intensity / (1 + fineness * math.pow(math.sin(delta / 2), 2))

            intensity[i][j] = light_intensity

    # color_scale = [(0, 'purple'), (0.13, 'blue'), (0.23, 'aqua'), (0.35, 'lime'),
    #                (0.55, 'yellow'), (0.7, 'red'), (0.9, 'red'), (1, 'maroon')]
    config = {'scrollZoom': True, 'toImageButtonOptions': {'height': None, 'width': None}}
    if laser_color == 'g':
        fig = px.imshow(intensity, color_continuous_scale=['#013b00', 'lime'])
    else:
        fig = px.imshow(intensity, color_continuous_scale=['#3b0000', 'red'])

    # print(px.colors.sequential.Inferno)
    graph = fig.to_html(full_html=False, config=config)
    return graph
