# Generated by Django 3.1.3 on 2020-11-24 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("content", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
                ("changed_at", models.DateField(auto_now=True)),
                ("end_at", models.DateField(blank=True, null=True)),
                ("add_vote", models.BooleanField(default=False)),
                ("is_locked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="DocumentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=128)),
            ],
            options={
                "verbose_name": "Types de document",
            },
        ),
    ]
