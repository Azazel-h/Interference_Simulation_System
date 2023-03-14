from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import ListView


class HistoryTableMixin(LoginRequiredMixin, ListView):
    model = None
    template_name = None
    context_object_name = None
    form = None
    object_list = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.model.objects

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        context = self.get_context_data()
        context[self.context_object_name] = self.get_queryset().filter(user=request.user.uid).order_by('-id')[:5]

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) -> TemplateResponse:
        history_form = self.form(request.POST)

        if history_form.is_valid():
            form_dict = dict(history_form.cleaned_data)
            form_dict['user'] = request.user.uid
            self.model.objects.create(**form_dict)

        return self.get(request)
