# Generated by Django 3.1.4 on 2020-12-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contributions", "0002_auto_20201124_1259"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(
                fields=("author", "document"), name="unique_vote"
            ),
        ),
    ]
