from django.shortcuts import render


def home_page(request) -> render:
    return render(request, 'pages/home.html')


def team_page(request) -> render:
    return render(request, 'pages/team.html')
