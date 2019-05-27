import csv
import io
import os
import pathlib
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from acm_placement_app.placements.forms import RUN_PARAMS_FIELDS, FACTOR_IMPORTANCE_FIELDS


def prepare_folders(run_timestamp):
    workspace_dir = get_workspace_location(run_timestamp)
    input_dir = os.path.join(workspace_dir, "input")
    output_dir = os.path.join(workspace_dir, "output")

    pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    return workspace_dir, input_dir, output_dir


def get_workspace_location(run_timestamp):
    location = os.path.join(settings.MEDIA_ROOT, 'tmp', 'taskspaces', str(run_timestamp))
    return location


def create_params_csv(fs, placementrequest):
    params_map = {
        field_name: str(getattr(placementrequest, field_name))
        for field_name in RUN_PARAMS_FIELDS + FACTOR_IMPORTANCE_FIELDS
    }
    with io.StringIO() as f:
        writer = csv.DictWriter(f, params_map.keys())
        writer.writeheader()
        writer.writerow(params_map)
        params_file_name = fs.save("params.csv", f)
        return fs.url(params_file_name)


def prepare_commutes_file(fs, placementrequest, commute_procedure_csv_string):
    commutes_reference_file_name = None
    if commute_procedure_csv_string:
        with io.StringIO() as f:
            f.write(commute_procedure_csv_string)
            commutes_reference_file_name = fs.save("commutes_reference_file.csv", f)

    elif placementrequest.commutes_reference_file:
        commutes_reference_file = placementrequest.commutes_reference_file.file
        commutes_reference_file_name = fs.save("commutes_reference_file.csv", commutes_reference_file)

    if commutes_reference_file_name:
        return fs.url(commutes_reference_file_name)
    return None


def prepare_workspace(placementrequest, run_timestamp, acm_df, commute_procedure_csv_string):
    workspace_dir, input_dir, output_dir = prepare_folders(run_timestamp)
    fs = FileSystemStorage(location=input_dir, base_url=input_dir)

    params_file_path = create_params_csv(fs, placementrequest)

    school_data_file = placementrequest.school_data_file.file
    school_data_file_name = fs.save("school_data_file.xlsx", school_data_file)
    school_data_file_path = fs.url(school_data_file_name)

    acm_survey_data_file_path = prepare_acm_survey_file(fs, acm_df)

    commutes_reference_file_path = prepare_commutes_file(fs, placementrequest, commute_procedure_csv_string)

    file_paths = (school_data_file_path, acm_survey_data_file_path, params_file_path, commutes_reference_file_path)

    return workspace_dir, file_paths, output_dir


def prepare_acm_survey_file(fs, acm_df):
    acm_df_csv_string = acm_df.to_csv(index=False)
    with io.StringIO() as acm_survey_data_file:
        acm_survey_data_file.write(acm_df_csv_string)
        acm_survey_data_file_name = fs.save("acm_survey_data_file.csv", acm_survey_data_file)
        return fs.url(acm_survey_data_file_name)


def clean_workspace(run_timestamp):
    location = os.path.join(settings.MEDIA_ROOT, 'tmp', 'taskspaces', str(run_timestamp))
    shutil.rmtree(location, ignore_errors=True)
