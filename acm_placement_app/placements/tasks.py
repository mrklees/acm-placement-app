import datetime
import pandas as pd
from celery import shared_task
from django.db import transaction

from acm_placement_app.placements.commutes import clean_commute_inputs, commute_procedure
from acm_placement_app.placements.models import PlacementsRequest
from acm_placement_app.placements.utils import clean_acm_file


@transaction.atomic
def process(placementsrequest):
    start_time = datetime.datetime.now()
    school_df = pd.read_excel(placementsrequest.school_data_file.file)
    acm_df = clean_acm_file(placementsrequest.acm_survey_data_file.file)

    if placementsrequest.calc_commutes:
        try:
            commute_schl_df = clean_commute_inputs(start_time, school_df,
                                                   placementsrequest.commute_date.strftime("%Y-%m-%d"))
            commute_procedure_csv_string = commute_procedure(commute_schl_df)
        except Exception as e:
            # TODO: Add errors to a field in request object
            return


@shared_task
def run_procedure(placements_request_id):
    placementsrequest = PlacementsRequest.objects.get(id=placements_request_id)

    process(placementsrequest)

    placementsrequest.is_completed = True
    placementsrequest.save()
