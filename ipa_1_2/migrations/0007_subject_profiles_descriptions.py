# Generated by Django 3.1.1 on 2021-08-12 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipa_1_2', '0006_auto_20210725_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='profiles_descriptions',
            field=models.TextField(blank=True),
        ),
    ]