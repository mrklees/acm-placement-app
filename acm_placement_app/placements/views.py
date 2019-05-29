import os
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from formtools.wizard.views import SessionWizardView

from acm_placement_app.placements.forms import PlacementRequestSchoolDataForm, PlacementRequestACMSurveyDataForm, \
    PlacementRequestRunParametersForm, PlacementRequestFactorImportanceForm, \
    get_placementrequest_instance_from_form_list
from acm_placement_app.placements.models import PlacementRequest, PlacementResult
from acm_placement_app.placements.tasks import run_procedure
from acm_placement_app.placements.utils import calculate_cost

FORMS = [
    ('school_data_form', PlacementRequestSchoolDataForm),
    ('acm_survey_data_form', PlacementRequestACMSurveyDataForm),
    ('run_parameters_form', PlacementRequestRunParametersForm),
    ('factor_importance_form', PlacementRequestFactorImportanceForm),
]

TEMPLATES = {
    'school_data_form': "wizard/school_data_form.html",
    'acm_survey_data_form': "wizard/acm_survey_data_form.html",
    'run_parameters_form': "wizard/run_parameters_form.html",
    'factor_importance_form': "wizard/factor_importance_form.html"
}


@method_decorator(login_required, name='dispatch')
class PlacementRequestWizard(SessionWizardView):
    form_list = FORMS
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp', 'wizard'))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        current_step = self.steps.current
        if current_step == 'run_parameters_form':
            acm_survey_data_form = self.get_form(step='acm_survey_data_form',
                                                 data=self.storage.get_step_data('acm_survey_data_form'),
                                                 files=self.storage.get_step_files('acm_survey_data_form'))
            context['warnings'] = acm_survey_data_form.get_warnings()

        return context

    def done(self, form_list, **kwargs):
        placementrequest = get_placementrequest_instance_from_form_list(form_list, commit=False)
        placementrequest.requested_by = self.request.user
        placementrequest.save()
        return HttpResponseRedirect(reverse('placements:run', kwargs={'id': placementrequest.id}))


@method_decorator(login_required, name='dispatch')
class RunView(View):
    def get(self, request, id):
        placementrequest = PlacementRequest.objects.get(id=id)
        # if placementrequest.is_completed:
        #     return render(request, "wizard/is_completed.html", context={'request': placementrequest})
        return render(request, "wizard/run.html", context=calculate_cost(placementrequest))

    def post(self, request, id):
        # placementrequest = PlacementRequest.objects.get(id=id)
        # if placementrequest.is_completed:
        #     return render(request, "wizard/is_completed.html", context={'request': placementrequest})
        run_procedure(id)
        return render(request, "wizard/done.html")


@method_decorator(login_required, name='dispatch')
class PlacementRequestList(ListView):
    context_object_name = 'placementrequests'
    template_name = "placements/request_list.html"
    queryset = PlacementRequest.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(requested_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class PlacementRequestDetail(DetailView):
    context_object_name = 'placementrequest'
    template_name = "placements/request_detail.html"
    queryset = PlacementRequest.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(requested_by=self.request.user)

@login_required
def download_results(request, pk=None):
    placementrequest = PlacementRequest.objects.get(id=pk)

    try:
        placementresult = placementrequest.placementresult
        response = HttpResponse(content_type='application/zip')
        zip_file_name = f"Request_{placementrequest.id}_results.zip"
        response['Content-Disposition'] = f'attachment; filename={zip_file_name}'
        with zipfile.ZipFile(response, 'w') as zip_file:
            write_file_to_zip(zip_file, placementrequest.school_data_file)
            write_file_to_zip(zip_file, placementrequest.acm_survey_data_file)
            write_file_to_zip(zip_file, placementresult.commutes_file)
            write_file_to_zip(zip_file, placementresult.placements_file)
            write_file_to_zip(zip_file, placementresult.trace_file)
        return response

    except PlacementResult.DoesNotExist:
        raise Http404


def write_file_to_zip(zip_file, file_obj):
    file_name = os.path.basename(file_obj.name)
    zip_file.writestr(file_name, file_obj.read())
