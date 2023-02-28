from django.http import HttpResponse
from django.views import View


class GraphMixin(View):
    form = None

    def post(self, request, *args, **kwargs) -> HttpResponse:
        graph = None
        form = self.form(request.POST)

        if form.is_valid():
            form_dict = dict(form.cleaned_data)
            graph = self.get_graph(form_dict)

        return HttpResponse(graph)

    @staticmethod
    def get_graph(form_dict: dict) -> str:
        return ""
