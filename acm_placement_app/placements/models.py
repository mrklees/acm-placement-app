import datetime

from django.db import models
from model_utils.models import TimeStampedModel


def get_tomorrow_date():
    return datetime.date.today() + datetime.timedelta(days=1)


class PlacementsRequest(TimeStampedModel, models.Model):
    school_data_file = models.FileField(upload_to='data/inputs/school_data/')
    acm_survey_data_file = models.FileField("ACM survey data file", upload_to='data/inputs/acm_survey_data/')

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
    commutes_reference = models.FileField(
        upload_to='documents/outputs',
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

