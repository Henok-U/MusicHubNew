# Generated by Django 4.1 on 2022-09-05 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*\\W).{8,}$"
                    )
                ],
            ),
        ),
    ]
