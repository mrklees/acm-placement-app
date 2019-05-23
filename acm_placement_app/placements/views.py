import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView

from acm_placement_app.placements.forms import PlacementsRequestSchoolDataForm, PlacementsRequestACMSurveyDataForm, \
    PlacementsRequestRunParametersForm, PlacementsRequestFactorImportanceForm

FORMS = [
    ('school_data_form', PlacementsRequestSchoolDataForm),
    ('acm_survey_data_file', PlacementsRequestACMSurveyDataForm),
    ('run_parameters_form', PlacementsRequestRunParametersForm),
    ('factor_importance_form', PlacementsRequestFactorImportanceForm),
]

TEMPLATES = {
    'school_data_form': "wizard/school_data_form.html",
    'acm_survey_data_file': "wizard/acm_survey_data_file.html",
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
        return context

    def done(self, form_list, **kwargs):
        school_data_form, acm_survey_data_file, run_parameters_form, factor_importance_form = form_list
        placementsrequest = run_parameters_form.instance
        placementsrequest.school_data_file = school_data_form.instance.school_data_file
        placementsrequest.acm_survey_data_file = acm_survey_data_file.instance.acm_survey_data_file

        placementsrequest.commute_factor = factor_importance_form.instance.commute_factor
        placementsrequest.ethnicity_factor = factor_importance_form.instance.ethnicity_factor
        placementsrequest.gender_factor = factor_importance_form.instance.gender_factor
        placementsrequest.edscore_factor = factor_importance_form.instance.edscore_factor
        placementsrequest.spanish_factor = factor_importance_form.instance.spanish_factor

        placementsrequest.save()

        return HttpResponse("Done!")
