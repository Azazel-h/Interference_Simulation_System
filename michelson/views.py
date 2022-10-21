from django.shortcuts import render
import plotly.express as px
from LightPipes import *
from .forms import GraphForm
import math
from django import forms


# def index(request):
#     return render(request, 'michelson/fabri-perot.html')

def index(request) -> render:
    context = {}
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            wavelength = form.cleaned_data['wavelength'] * nm
            R = form.cleaned_data['R'] * mm
            z1 = form.cleaned_data['z1'] * cm
            z2 = form.cleaned_data['z2'] * cm
            z3 = form.cleaned_data['z3'] * cm
            z4 = form.cleaned_data['z4'] * cm
            Rbs = form.cleaned_data['Rbs']
            tx = form.cleaned_data['tx'] * mrad
            ty = form.cleaned_data['ty'] * mrad
            f = form.cleaned_data['f'] * cm
            size = form.cleaned_data['size'] * mm
            N = form.cleaned_data['N']

            graph = get_graph(wavelength, R, z1, z2, z3, z4, Rbs, tx, ty, f, size, N)
            context['graph'] = graph
        else:
            form = GraphForm()
        context['form'] = form
    return render(request, 'michelson/../templates/pages/michelson.html', context=context)


def get_graph(wavelength, R, z1, z2, z3, z4, Rbs, tx, ty, f, size, N):
    # wavelength = 632.8 * nm  # wavelength of HeNe laser
    # R = 3 * mm  # laser beam radius
    # z1 = 8 * cm  # length of arm 1
    # z2 = 7 * cm  # length of arm 2
    # z3 = 3 * cm  # distance laser to beamsplitter
    # z4 = 5 * cm  # distance beamsplitter to screen
    # Rbs = 0.5  # reflection beam splitter
    # tx = 1 * mrad
    # ty = 0.0 * mrad  # tilt of mirror 1
    # f = 50 * cm  # focal length of positive lens
    # size = 10 * mm  # size of the grid
    # N = 300  # number (NxN) of grid pixels

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
    fig = px.imshow(I)

    # print(px.colors.sequential.Inferno)
    graph = fig.to_html(full_html=False)
    return graph
