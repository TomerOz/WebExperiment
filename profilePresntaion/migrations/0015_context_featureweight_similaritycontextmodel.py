# Generated by Django 3.1.1 on 2021-02-04 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profilePresntaion', '0014_auto_20210102_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Neutral', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SimilarityContextModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilePresntaion.featurelabels')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0.5)),
                ('feature_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilePresntaion.featurelabels')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilePresntaion.similaritycontextmodel')),
            ],
        ),
    ]