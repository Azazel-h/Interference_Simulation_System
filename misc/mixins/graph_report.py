import io

import docx

from typing import Optional
from django.http import HttpResponse, FileResponse
from django.views import View
from plotly.graph_objs import Figure
from docx.shared import Cm


class GraphReportMixin(View):
    form = None

    def post(self, request, *args, **kwargs) -> Optional[HttpResponse]:
        form = self.form(request.POST)

        if form.is_valid():
            form_dict = dict(form.cleaned_data)
            graph = self.get_graph(form_dict)

            doc = docx.Document()

            graph_png = io.BytesIO(graph.to_image(format='png'))
            doc.add_picture(graph_png, width=Cm(15.75), height=Cm(11.25))

            target_stream = io.BytesIO()
            doc.save(target_stream)
            target_stream.seek(0)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="filename.docx"'

            response.write(target_stream.read())
            target_stream.close()
            graph_png.close()

            return response

    @staticmethod
    def get_graph(form_dict: dict) -> Optional[Figure]:
        return None
