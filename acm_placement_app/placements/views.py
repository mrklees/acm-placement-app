import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from acm_placement_app.placements.forms import PlacementsRequestSchoolDataForm, PlacementsRequestACMSurveyDataForm, \
    PlacementsRequestRunParametersForm, PlacementsRequestFactorImportanceForm, FACTOR_IMPORTANCE_FIELDS

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
        get_placementrequest_instance_from_form_list(form_list).save()
        return render(self.request, "wizard/done.html")


def get_placementrequest_instance_from_form_list(form_list):
    school_data_form, acm_survey_data_form, run_parameters_form, factor_importance_form = form_list
    placementsrequest = run_parameters_form.save(commit=False)

    # Uploaded files
    placementsrequest.school_data_file = school_data_form.instance.school_data_file
    placementsrequest.acm_survey_data_file = acm_survey_data_form.instance.acm_survey_data_file

    # Factor importances
    if factor_importance_form.is_valid():
        for field_name in FACTOR_IMPORTANCE_FIELDS:
            setattr(placementsrequest, field_name, factor_importance_form.cleaned_data[field_name])

    return placementsrequest
