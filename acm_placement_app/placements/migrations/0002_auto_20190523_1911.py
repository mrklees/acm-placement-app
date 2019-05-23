# Generated by Django 2.1.8 on 2019-05-23 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('placements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='placementsrequest',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='placementsrequest',
            name='acm_survey_data_file',
            field=models.FileField(upload_to='data/inputs/acm_survey_data/', verbose_name='ACM survey data file'),
        ),
    ]
