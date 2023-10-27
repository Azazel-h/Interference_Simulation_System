from typing import Optional
from django.http import HttpResponse
from django.views import View
from plotly.graph_objs import Figure


class GraphMixin(View):
    form = None

    def post(self, request, *args, **kwargs) -> Optional[HttpResponse]:
        form = self.form(request.POST)

        if form.is_valid():
            form_dict = dict(form.cleaned_data)
            graph = self.get_graph(form_dict)
            config = {
                'displaylogo': False,
                'toImageButtonOptions': {
                    'height': None,
                    'width': None
                }
            }
            return HttpResponse(graph.to_html(config=config, include_plotlyjs=False, full_html=False))

    @staticmethod
    def get_graph(form_dict: dict) -> Optional[Figure]:
        return None
