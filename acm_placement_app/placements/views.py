import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView

from acm_placement_app.placements.forms import PlacementsRequestSchoolDataForm, PlacementsRequestACMSurveyDataForm, \
    PlacementsRequestRunParametersForm
from acm_placement_app.placements.models import PlacementsRequest


# def instance_update(instance1, instance2, keys):
#     instance2_dict = {k: v for k, v in instance2.__dict__.items() if v in keys}
#     instance1.__dict__.update(instance2_dict)


class PlacementsRequestWizard(SessionWizardView):
    form_list = [
        PlacementsRequestSchoolDataForm,
        PlacementsRequestACMSurveyDataForm,
        PlacementsRequestRunParametersForm
    ]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp', 'wizard'))

    def done(self, form_list, **kwargs):
        step1, step2, step3 = form_list
        placementsrequest = step3.instance
        placementsrequest.school_data_file = step1.instance.school_data_file
        placementsrequest.acm_survey_data_file = step2.instance.acm_survey_data_file
        placementsrequest.save()
        
        return HttpResponse("Done!")

