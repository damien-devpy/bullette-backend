# Generated by Django 3.1.4 on 2020-12-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contributions", "0006_auto_20201210_1400"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="edit_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
