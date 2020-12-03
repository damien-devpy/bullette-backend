# Generated by Django 3.1.3 on 2020-11-24 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contributions', '0002_auto_20201124_1259'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='comments',
            field=models.ManyToManyField(related_name='document_comments', through='contributions.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='documents.documenttype'),
        ),
        migrations.AddField(
            model_name='document',
            name='votes',
            field=models.ManyToManyField(related_name='document_votes', through='contributions.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
