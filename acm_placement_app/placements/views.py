import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from formtools.wizard.views import SessionWizardView

from acm_placement_app.placements.forms import PlacementsRequestSchoolDataForm, PlacementsRequestACMSurveyDataForm, \
    PlacementsRequestRunParametersForm, PlacementsRequestFactorImportanceForm, \
    get_placementrequest_instance_from_form_list
from acm_placement_app.placements.models import PlacementsRequest
from acm_placement_app.placements.tasks import run_procedure
from acm_placement_app.placements.utils import calculate_cost

FORMS = [
    ('school_data_form', PlacementsRequestSchoolDataForm),
    ('acm_survey_data_form', PlacementsRequestACMSurveyDataForm),
    ('run_parameters_form', PlacementsRequestRunParametersForm),
    ('factor_importance_form', PlacementsRequestFactorImportanceForm),
]

TEMPLATES = {
    'school_data_form': "wizard/school_data_form.html",
    'acm_survey_data_form': "wizard/acm_survey_data_form.html",
    'run_parameters_form': "wizard/run_parameters_form.html",
    'factor_importance_form': "wizard/factor_importance_form.html"
}


@method_decorator(login_required, name='dispatch')
class PlacementsRequestWizard(SessionWizardView):
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
        placementsrequest = get_placementrequest_instance_from_form_list(form_list, commit=False)
        placementsrequest.requested_by = self.request.user
        placementsrequest.save()
        return HttpResponseRedirect(reverse('placements:run', kwargs={'id': placementsrequest.id}))


@method_decorator(login_required, name='dispatch')
class RunView(View):
    def get(self, request, id):
        placementsrequest = PlacementsRequest.objects.get(id=id)
        return render(request, "wizard/run.html", context=calculate_cost(placementsrequest))

    def post(self, request, id):
        run_procedure(id)
        return render(request, "wizard/done.html")
