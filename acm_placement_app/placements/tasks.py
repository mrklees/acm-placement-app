import time

import pandas as pd
from celery import shared_task
from django.db import transaction

from acm_placement_app.placements.commutes import clean_commute_inputs, commute_procedure
from acm_placement_app.placements.models import PlacementRequest
from acm_placement_app.placements.task_utils import prepare_workspace, clean_workspace
from acm_placement_app.placements.utils import clean_acm_file


@transaction.atomic
def process(placementrequest, run_timestamp):
    # start_time = datetime.datetime.now()

    school_df = pd.read_excel(placementrequest.school_data_file.file)
    acm_df = clean_acm_file(placementrequest.acm_survey_data_file.file)
    commute_procedure_csv_string = None

    if placementrequest.calc_commutes:
        commute_schl_df = clean_commute_inputs(acm_df, school_df,
                                               placementrequest.commute_date.strftime("%Y-%m-%d"))
        if not placementrequest.commutes_reference_file:
            commute_procedure_csv_string = commute_procedure(commute_schl_df)

    school_data_file_url, acm_survey_data_file_url, params_file_url, commutes_reference_file_url = prepare_workspace(
        placementrequest, run_timestamp, commute_procedure_csv_string
    )
    # os.system(f'Rscript --no-restore --no-save launch_alg.R > {error_path} 2>&1')


@shared_task
def run_procedure(placements_request_id):
    run_timestamp = int(time.time())
    placementrequest = PlacementRequest.objects.get(id=placements_request_id)

    try:
        process(placementrequest, run_timestamp)
        placementrequest.is_completed = True

    except Exception as e:
        # TODO: Add errors to a field in request object
        placementrequest.errors = str(e)
    finally:
        clean_workspace(run_timestamp)

    placementrequest.save()
