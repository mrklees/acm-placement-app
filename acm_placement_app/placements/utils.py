import os

import numpy as np
import pandas as pd


def get_acm_survey_missing_columns(acm_file):
    acm_df = pd.read_csv(acm_file)
    vars_df = pd.read_excel(os.path.join("data_files", "Survey Items to Variable Names.xlsx"))

    # trim whitespace from headers
    acm_df.columns = acm_df.columns.str.strip()
    vars_df['SurveyGizmo Column Name'] = vars_df['SurveyGizmo Column Name'].str.strip()

    rename_dict = dict(zip(vars_df['SurveyGizmo Column Name'], vars_df['Expected Column Name']))
    acm_df.rename(columns=rename_dict, inplace=True)

    missing_columns = [x for x in vars_df.loc[vars_df['Required?'] == 'Required', 'Expected Column Name'] if
                       x not in acm_df.columns]
    return acm_df, missing_columns


def clean_acm_file(acm_file):
    acm_df, missing_columns = get_acm_survey_missing_columns(acm_file)
    for x in missing_columns:
        acm_df[x] = np.nan

    acm_df['Res.Postal.Code'] = acm_df['Res.Postal.Code'].astype(str)
    acm_df.loc[acm_df['Res.Postal.Code'] == 'nan', 'Res.Postal.Code'] = np.nan
    acm_df['Res.Address.Line.1'] = acm_df['Res.Address.Line.1'].str.upper().str.split('#|APT|UNIT', 1).str[0]
    acm_df['Home_Address'] = acm_df[['Res.Address.Line.1', 'Res.City', 'Res.State', 'Res.Postal.Code']].apply(
        lambda x: x.str.cat(sep=' '), axis=1)

    return acm_df


def calculate_cost(placementsrequest):
    school_df = pd.read_excel(placementsrequest.school_data_file.file)
    acm_df = clean_acm_file(placementsrequest.acm_survey_data_file.file)

    n_acms = len(acm_df)
    n_schools = len(school_df)

    run_time = 12  # in seconds, base time required for 1 iteration and no commutes
    run_time += placementsrequest.num_iterations / 4.38  # 4.38 iterations per second

    if placementsrequest.calc_commutes:
        # TODO: Clean file
        n_acm_addresses = len(acm_df.loc[~acm_df['Home_Address'].isnull() & (acm_df['Home_Address'] != '')])

        and_text = ' and calculating commutes'
        and_cost_text = ' and cost HQ '
        and_cost = f'${round(n_acm_addresses * n_schools * 0.005, 2)}'

        run_time += (n_acm_addresses * n_schools) / 1.73  # 1.73 API requests per second
    else:
        and_text, and_cost_text, and_cost = '', '', ''

    run_time_mins = round(run_time / 60, 1)

    return {
        'n_acms': n_acms,
        'n_schools': n_schools,
        'run_time_mins': run_time_mins,
        'and_text': and_text,
        'and_cost_text': and_cost_text,
        'and_cost': and_cost
    }
