# Generated by Django 3.1.4 on 2020-12-10 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0004_auto_20201210_0759'),
        ('documents', '0004_document_votes_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='edit_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='votes_values',
            field=models.ManyToManyField(blank=True, to='contributions.VoteValue'),
        ),
    ]
