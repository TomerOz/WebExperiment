# Generated by Django 3.1.1 on 2021-03-29 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilePresntaion', '0018_auto_20210329_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='current_phase',
        ),
    ]
