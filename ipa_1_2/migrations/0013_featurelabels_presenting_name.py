# Generated by Django 3.1.1 on 2021-08-15 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipa_1_2', '0012_featurelabels_question_heb'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurelabels',
            name='presenting_name',
            field=models.CharField(default='Default Name', max_length=200),
        ),
    ]