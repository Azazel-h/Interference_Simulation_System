from django.shortcuts import render
import plotly.express as px
from LightPipes import *
import math
from .forms import GraphForm


def index_page(request) -> render:
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            labda = form.cleaned_data['labda'] * nm
            size = form.cleaned_data['size'] * mm

            N = form.cleaned_data['N']
            f = form.cleaned_data['f'] * mm
            k = form.cleaned_data['k'] * math.pi / labda
            D = form.cleaned_data['D']
            R = form.cleaned_data['R']

            DLABDA = form.cleaned_data['DLABDA'] / nm
            NMEDIUM = form.cleaned_data['NMEDIUM']

            graph = get_graph(DLABDA, NMEDIUM, labda, size, N, D, R, f, k)
    else:
        form = GraphForm()
        graph = ''
    return render(request, 'index.html', context={'graph': graph, 'form': form})

def get_graph(DLABDA, NMEDIUM, labda, size, N, D, R, f, k):
    global I
    Dlabda = DLABDA * nm
    nmedium = NMEDIUM
    d = D * mm
    r = R
    k2 = 2 * math.pi / (labda + Dlabda)
    Fin = 4.0 * r / (1.0 - r)
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

            delta2 = k * nmedium * d * math.cos(theta)
            Inten = 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2))
            delta2 = k2 * nmedium * d * math.cos(theta)

            I[i][j] = (Inten + 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2)))
    fig = px.imshow(I)
    graph = fig.to_html(full_html=False)

    return graph
