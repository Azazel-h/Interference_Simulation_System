import math

import plotly.express as px
from LightPipes import *
from django.shortcuts import render
from .models import RequestFP

from .forms import GraphForm


def index_page(request) -> render:
    context = {}
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            picture_size = form.cleaned_data['picture_size'] * mm
            focal_distance = form.cleaned_data['focal_distance'] * mm
            glasses_distance = form.cleaned_data['glasses_distance'] * mm
            stroke_difference = form.cleaned_data['stroke_difference'] * nm
            reflectivity = form.cleaned_data['reflectivity']
            refractive_index = form.cleaned_data['refractive_index']
            incident_light_intensity = form.cleaned_data['incident_light_intensity'] * W / cm / cm
            color = form.cleaned_data['laser_color']
            n = form.cleaned_data['N']

            RequestFP.objects.create(user=request.user.username,
                                     laser_color=form.cleaned_data['laser_color'],
                                     glasses_distance=form.cleaned_data['glasses_distance'],
                                     focal_distance=form.cleaned_data['focal_distance'],
                                     stroke_difference=form.cleaned_data['stroke_difference'],
                                     reflectivity=form.cleaned_data['reflectivity'],
                                     refractive_index=form.cleaned_data['refractive_index'],
                                     picture_size=form.cleaned_data['picture_size'],
                                     incident_light_intensity=form.cleaned_data['incident_light_intensity'],
                                     N=form.cleaned_data['N'])

            if color == 'g':
                wave_length = 532 * nm
            else:
                wave_length = 630 * nm

            # incident_light_intensity = 10

            graph = get_graph(stroke_difference, refractive_index, wave_length, picture_size,
                              n, glasses_distance, reflectivity, focal_distance, incident_light_intensity, color)
            context['graph'] = graph
    else:
        form = GraphForm()

    user_requests = RequestFP.objects.filter(user=request.user.username)[::-1]
    context['array_of_reqs'] = user_requests[:5]
    context['form'] = form
    return render(request, 'pages/fabri-perot.html', context=context)


def get_graph(stroke_difference, refractive_index, wave_length, picture_size, n,
              glasses_distance, reflectivity, focal_distance, incident_light_intensity, laser_color):
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
