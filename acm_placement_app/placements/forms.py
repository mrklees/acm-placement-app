import os

import pandas as pd
from django import forms

from acm_placement_app.placements.models import PlacementsRequest

BLANK_COLS_WARNING_MSG = """Warning: the following columns could not be resolved from your survey file. 
These columns will be filled with blanks if you choose to continue:"""


class PlacementsRequestSchoolDataForm(forms.ModelForm):
    class Meta:
        model = PlacementsRequest
        fields = [
            'school_data_file'
        ]


class PlacementsRequestACMSurveyDataForm(forms.ModelForm):
    def missing_columns(self):
        acm_df = pd.read_csv(self.files['acm_survey_data_form-acm_survey_data_file'])
        vars_df = pd.read_excel(os.path.join("data_files", "Survey Items to Variable Names.xlsx"))

        # trim whitespace from headers
        acm_df.columns = acm_df.columns.str.strip()
        vars_df['SurveyGizmo Column Name'] = vars_df['SurveyGizmo Column Name'].str.strip()

        rename_dict = dict(zip(vars_df['SurveyGizmo Column Name'], vars_df['Expected Column Name']))
        acm_df.rename(columns=rename_dict, inplace=True)

        return [x for x in vars_df.loc[vars_df['Required?'] == 'Required', 'Expected Column Name']
                if x not in acm_df.columns]

    def get_warnings(self):
        warnings = {}
        if True:
            warnings['message'] = BLANK_COLS_WARNING_MSG
            warnings['list'] = self.missing_columns()
        return warnings

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
        ]


class PlacementsRequestFactorImportanceForm(forms.ModelForm):
    class Meta:
        model = PlacementsRequest
        fields = [
            'commute_factor',
            'ethnicity_factor',
            'gender_factor',
            'edscore_factor',
            'spanish_factor',
        ]
