import os
import subprocess
import time

import pandas as pd
from celery import shared_task
from django.conf import settings
from django.db import transaction

from acm_placement_app.placements.commutes import clean_commute_inputs, commute_procedure
from acm_placement_app.placements.models import PlacementRequest
from acm_placement_app.placements.task_utils import prepare_workspace, clean_workspace
from acm_placement_app.placements.utils import clean_acm_file

R_SCRIPTS_PATH = os.path.join(settings.ROOT_DIR, 'r_scripts')
LAUNCH_ALG_SCRIPT = os.path.join(R_SCRIPTS_PATH, 'launch_alg.R')


@transaction.atomic
def process(placementrequest, run_timestamp):
    school_df = pd.read_excel(placementrequest.school_data_file.file)
    acm_df = clean_acm_file(placementrequest.acm_survey_data_file.file)
    commute_procedure_csv_string = None

    if placementrequest.calc_commutes:
        commute_schl_df = clean_commute_inputs(acm_df, school_df,
                                               placementrequest.commute_date.strftime("%Y-%m-%d"))
        if not placementrequest.commutes_reference_file:
            commute_procedure_csv_string = commute_procedure(commute_schl_df)

    workspace_dir, file_paths, output_dir = prepare_workspace(placementrequest, run_timestamp,
                                                              acm_df, commute_procedure_csv_string)
    r_logs_path = os.path.join(workspace_dir, "r_logs")

    r_script = " ".join([
        "Rscript --no-restore --no-save",
        f"{LAUNCH_ALG_SCRIPT} {' '.join(file_paths)} {output_dir} {R_SCRIPTS_PATH}",
        f"> {r_logs_path} 2>&1"
    ])
    print(r_script)
    subprocess.call(r_script, shell=True)
    with open(r_logs_path) as f:
        errors = f.read()
        if "Execution halted" in errors:
            raise Exception(errors)


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
        pass
        # clean_workspace(run_timestamp)

    placementrequest.save()
