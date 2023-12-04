from typing import Optional, Union

from django.http import JsonResponse
from django.views import View


class GraphMixin(View):
    form = None

    def post(self, request, *args, **kwargs) -> JsonResponse:
        graph = None
        form = self.form(request.POST)

        if form.is_valid():
            form_dict = dict(form.cleaned_data)
            graph = self.get_graph(form_dict)

        return JsonResponse(graph, safe=False)

    @staticmethod
    def get_graph(form_dict: dict) -> Optional[dict[str, Union[str, tuple[str, ...]]]]:
        return None
