from django.shortcuts import render


def home_page(request) -> render:
    return render(request, 'pages/home.html')
