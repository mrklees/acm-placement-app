import datetime
import os

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


def get_tomorrow_date():
    return datetime.date.today() + datetime.timedelta(days=1)


def input_upload_path(instance, filename):
    return os.path.join("data", 'inputs', filename)


def output_upload_path(instance, filename):
    return os.path.join("data", 'outputs', filename)


class PlacementRequest(TimeStampedModel, models.Model):
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    school_data_file = models.FileField(upload_to=input_upload_path)
    acm_survey_data_file = models.FileField("ACM survey data file", upload_to=input_upload_path)

    num_iterations = models.IntegerField(
        "Number of iterations", default=10000,
        help_text="The number of team placements that will be attempted. 10,000 or more is recommended."
    )
    prevent_roommates = models.BooleanField("Prevent roommates from serving on the same team?", default=True)
    consider_HS_elig = models.BooleanField(
        "Apply High School eligibility rule?", default=True,
        help_text="ACMs are eligible to serve in High School if they are 21+ years old (or have college experience) "
                  "and are confident tutoring at least algebra-level math."
    )

    calc_commutes = models.BooleanField(
        "Calculate commutes?", default=True,
        help_text="Commute calculations cost HQ a small amount and take time to complete. "
                  "For 100 ACMs and 10 schools, the cost is $5 and takes about 10 minutes."
    )
    commute_date = models.DateField(
        "Travel date for commute calculations", blank=True, default=get_tomorrow_date,
        help_text="Required if calculating commutes. Choose a date that represents normal traffic."
    )
    commutes_reference_file = models.FileField(
        upload_to=input_upload_path,
        blank=True,
        help_text="After placements are made, you will find a 'Output_Commute_Reference.csv' file in the results. "
                  "If you want to run additional placement processes, "
                  "upload that file here to avoid commute calculation wait time and cost."
    )

    # --- FACTORS --- #
    commute_factor = models.IntegerField("Importance of commute", default=1)
    ethnicity_factor = models.IntegerField("Importance of ethnic diversity", default=1)
    gender_factor = models.IntegerField("Importance of gender diversity", default=1)
    edscore_factor = models.IntegerField("Importance of educational attainment diversity", default=1)
    spanish_factor = models.IntegerField("Importance of matching Spanish speaker targets", default=1)

    # errors
    errors = models.TextField(blank=True)


class PlacementResult(TimeStampedModel, models.Model):
    placementrequest = models.OneToOneField(PlacementRequest, on_delete=models.CASCADE)

    commutes_file = models.FileField(upload_to=output_upload_path)
    placements_file = models.FileField(upload_to=output_upload_path)
    trace_file = models.FileField(upload_to=output_upload_path)
