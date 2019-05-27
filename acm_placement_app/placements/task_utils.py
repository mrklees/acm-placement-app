import csv
import io
import os
import pathlib
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from acm_placement_app.placements.forms import RUN_PARAMS_FIELDS, FACTOR_IMPORTANCE_FIELDS


def prepare_folders(run_timestamp):
    location = get_workspace_location(run_timestamp)
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)
    return location


def get_workspace_location(run_timestamp):
    location = os.path.join(settings.MEDIA_ROOT, 'tmp', 'taskspaces', str(run_timestamp))
    return location


def create_params_csv(fs, placementsrequest):
    params_map = {
        field_name: str(getattr(placementsrequest, field_name))
        for field_name in RUN_PARAMS_FIELDS + FACTOR_IMPORTANCE_FIELDS
    }
    with io.StringIO() as f:
        writer = csv.DictWriter(f, params_map.keys())
        writer.writeheader()
        writer.writerow(params_map)
        params_file_name = fs.save("params.csv", f)
        return fs.url(params_file_name)


def prepare_commutes_file(fs, placementsrequest, commute_procedure_csv_string):
    commutes_reference_file_name = None
    if commute_procedure_csv_string:
        with io.StringIO() as f:
            f.write(commute_procedure_csv_string)
            commutes_reference_file_name = fs.save("commutes_reference_file.xlsx", f)

    elif placementsrequest.commutes_reference_file:
        commutes_reference_file = placementsrequest.commutes_reference_file.file
        commutes_reference_file_name = fs.save("commutes_reference_file.xlsx", commutes_reference_file)

    if commutes_reference_file_name:
        return fs.url(commutes_reference_file_name)
    return None


def prepare_workspace(placementsrequest, run_timestamp, commute_procedure_csv_string):
    location = prepare_folders(run_timestamp)
    fs = FileSystemStorage(location=location, base_url=location)

    params_file_url = create_params_csv(fs, placementsrequest)

    school_data_file = placementsrequest.school_data_file.file
    school_data_file_name = fs.save("school_data_file.xlsx", school_data_file)
    school_data_file_url = fs.url(school_data_file_name)

    acm_survey_data_file = placementsrequest.acm_survey_data_file.file
    acm_survey_data_file_name = fs.save("acm_survey_data_file.xlsx", acm_survey_data_file)
    acm_survey_data_file_url = fs.url(acm_survey_data_file_name)

    commutes_reference_file_url = prepare_commutes_file(fs, placementsrequest, commute_procedure_csv_string)

    return school_data_file_url, acm_survey_data_file_url, params_file_url, commutes_reference_file_url


def clean_workspace(run_timestamp):
    location = os.path.join(settings.MEDIA_ROOT, 'tmp', 'taskspaces', str(run_timestamp))
    shutil.rmtree(location, ignore_errors=True)
