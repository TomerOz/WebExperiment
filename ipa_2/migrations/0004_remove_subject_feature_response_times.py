# Generated by Django 3.1.1 on 2022-08-09 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipa_2', '0003_auto_20220803_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='feature_response_times',
        ),
    ]
