from django.shortcuts import render
import plotly.express as px
from LightPipes import *
import math
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
            color = form.cleaned_data['laser_color']

            if color == 'g':
                wave_length = 532 * nm
            else:
                wave_length = 630 * nm

            N = form.cleaned_data['N']

            k = 2 * math.pi / wave_length

            graph = get_graph(stroke_difference, refractive_index, wave_length, picture_size,
                              N, glasses_distance, reflectivity, focal_distance, k, color)
            context['graph'] = graph
    else:
        form = GraphForm()
    context['form'] = form
    return render(request, 'index.html', context=context)


def get_graph(stroke_difference, refractive_index, wave_length, picture_size, N,
              glasses_distance, reflectivity, focal_distance, k, laser_color):
    second_k = 2 * math.pi / (wave_length + stroke_difference)
    fineness = 4.0 * reflectivity / (1.0 - reflectivity)

    F = Begin(picture_size, wave_length, N)
    I = Intensity(F, 1)

    step = picture_size / N / mm
    for i in range(1, N):
        x_ray = i * step
        for j in range(1, N):
            y_ray = j * step

            X = x_ray * mm - picture_size / 2
            Y = y_ray * mm - picture_size / 2

            radius = math.sqrt(X * X + Y * Y)
            theta = radius / focal_distance

            delta = 2 * k * refractive_index * glasses_distance * math.cos(theta)
            Intensivity = 1 / (1 + fineness * math.pow(math.sin(delta / 2), 2))

            delta = 2 * second_k * refractive_index * glasses_distance * math.cos(theta)
            I[i][j] = (Intensivity + 1 / (1 + fineness * math.pow(math.sin(delta / 2), 2)))

    # color_scale = [(0, 'purple'), (0.13, 'blue'), (0.23, 'aqua'), (0.35, 'lime'),
    #              (0.55, 'yellow'), (0.7, 'red'), (0.9, 'red'), (1, 'maroon')]
    config = {'scrollZoom': True, 'toImageButtonOptions': {'height': None, 'width': None}}
    if laser_color == 'g':
        fig = px.imshow(I, color_continuous_scale=[(0, '#013b00'), (1, 'lime')])
    else:
        fig = px.imshow(I, color_continuous_scale=[(0, '#3b0000'), (1, 'red')])

    # print(px.colors.sequential.Inferno)
    graph = fig.to_html(full_html=False, config=config)
    return graph
