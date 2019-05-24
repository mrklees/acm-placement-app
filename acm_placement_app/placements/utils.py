import pandas as pd


def calculate_cost(placementsrequest):
    school_df = pd.read_excel(placementsrequest.school_data_file.file)
    acm_df = pd.read_csv(placementsrequest.acm_survey_data_file.file)

    n_acms = len(acm_df)
    n_schools = len(school_df)

    run_time = 12  # in seconds, base time required for 1 iteration and no commutes
    run_time += placementsrequest.num_iterations / 4.38  # 4.38 iterations per second

    if placementsrequest.calc_commutes:
        # TODO: Clean file
        n_acm_addresses = 0  # len(acm_df.loc[~acm_df['Home_Address'].isnull() & (acm_df['Home_Address'] != '')])

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
