# Generated by Django 5.2.4 on 2025-07-16 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="end_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
