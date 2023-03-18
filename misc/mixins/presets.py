from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import ListView


class PresetsTableMixin(LoginRequiredMixin, ListView):
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
        context[self.context_object_name] = self.model.objects.filter(user=request.user.uid).order_by('-id')

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) -> TemplateResponse:
        if request.POST.get('preset_operation') == 'save_preset':
            form = self.form(request.POST)

            if form.is_valid():
                form_dict = dict(form.cleaned_data)
                form_dict['user'] = request.user.uid

                if len(self.model.objects.filter(user=request.user.uid)) < 5:
                    self.model.objects.create(**form_dict)
        elif request.POST.get('preset_operation') == 'delete_preset':
            self.model.objects.get(id=request.POST.get('delete_preset')).delete()

        return self.get(request)