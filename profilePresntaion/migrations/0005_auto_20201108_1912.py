# Generated by Django 3.1.1 on 2020-11-08 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profilePresntaion', '0004_auto_20201108_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='str_phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilePresntaion.experimentphase'),
        ),
    ]
