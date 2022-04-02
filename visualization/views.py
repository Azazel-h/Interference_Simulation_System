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
            labda = form.cleaned_data['labda'] * nm
            size = form.cleaned_data['size'] * mm

            N = form.cleaned_data['N']
            f = form.cleaned_data['f'] * mm
            k = form.cleaned_data['k'] * math.pi / labda
            D = form.cleaned_data['D'] * mm
            R = form.cleaned_data['R']

            DLABDA = form.cleaned_data['DLABDA'] * nm
            NMEDIUM = form.cleaned_data['NMEDIUM']

            graph = get_graph(DLABDA, NMEDIUM, labda, size, N, D, R, f, k)
            context['graph'] = graph
    else:
        form = GraphForm()
    context['form'] = form
    
    return render(request, 'index.html', context=context)

def get_graph(DLABDA, NMEDIUM, labda, size, N, D, R, f, k):
    k2 = 2 * math.pi / (labda + DLABDA)
    Fin = 4.0 * R / (1.0 - R)
    F = Begin(size, labda, N)

    I = Intensity(F, 1)
    step = size / N / mm
    for i in range(1, N):
        xray = i * step
        for j in range(1, N):
            yray = j * step

            X = xray * mm - size / 2
            Y = yray * mm - size / 2

            radius = math.sqrt(X * X + Y * Y)
            theta = radius / f

            delta2 = k * NMEDIUM * D * math.cos(theta)
            Inten = 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2))
            delta2 = k2 * NMEDIUM * D * math.cos(theta)

            I[i][j] = (Inten + 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2)))
    fig = px.imshow(I)
    graph = fig.to_html(full_html=False)

    return graph
