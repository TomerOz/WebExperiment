# Generated by Django 3.1.1 on 2022-07-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipa_2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='sets_order',
            field=models.CharField(default='A,C', max_length=50),
        ),
    ]
