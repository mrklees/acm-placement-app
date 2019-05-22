from django import forms

from acm_placement_app.placements.models import PlacementsRequest


class PlacementsRequestSchoolDataForm(forms.ModelForm):
    class Meta:
        model = PlacementsRequest
        fields = [
            'school_data_file'
        ]


class PlacementsRequestACMSurveyDataForm(forms.ModelForm):
    class Meta:
        model = PlacementsRequest
        fields = [
            'acm_survey_data_file'
        ]


class PlacementsRequestRunParametersForm(forms.ModelForm):
    class Meta:
        model = PlacementsRequest
        fields = [
            'num_iterations',
            'prevent_roommates',
            'consider_HS_elig',
            'calc_commutes',
            'commute_date',
            'commutes_reference',
            'commute_factor',
            'ethnicity_factor',
            'gender_factor',
            'edscore_factor',
            'spanish_factor',
        ]
