# Generated by Django 3.2.18 on 2023-05-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_explore_common_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="blob_url",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
