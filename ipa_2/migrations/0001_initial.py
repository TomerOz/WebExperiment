# Generated by Django 3.1.1 on 2022-12-23 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('phases', models.CharField(default='pre task, post task', max_length=30)),
                ('n_identification_rounds_allowed', models.IntegerField(default=2)),
                ('dubbled_artificials_list', models.CharField(default='0.2, 0.4, 0.6, 0.8', max_length=100)),
                ('subject_bonuses', models.TextField(default='9999-0,')),
                ('ps_l_A', models.IntegerField(default=15)),
                ('ps_h_A', models.IntegerField(default=15)),
                ('ps_l_C', models.IntegerField(default=15)),
                ('ps_h_C', models.IntegerField(default=15)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('phase_place', models.IntegerField()),
                ('n_trials', models.IntegerField(default=999)),
                ('n_practice_trials', models.IntegerField(default=999)),
                ('practice_trials_content', models.CharField(default='0.2, 0.5', max_length=1000)),
                ('trials_content', models.CharField(default='0.2, 0.5', max_length=1000)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.experiment')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureLabels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right_end', models.CharField(default='right', max_length=200)),
                ('left_end', models.CharField(default='left', max_length=200)),
                ('feature_name', models.CharField(default='Name', max_length=200)),
                ('label_set', models.CharField(default='A', max_length=2)),
                ('question_heb_male', models.CharField(default='Default question?', max_length=200)),
                ('question_heb_female', models.CharField(default='Default question?', max_length=200)),
                ('question_heb_max_min_ideal_male', models.CharField(default='Default question?', max_length=200)),
                ('question_heb_max_min_ideal_female', models.CharField(default='Default question?', max_length=200)),
                ('presenting_name', models.CharField(default='Default Name', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_subject', models.BooleanField(default=False)),
                ('is_artificial', models.BooleanField(default=False)),
                ('is_MinMax', models.BooleanField(default=False)),
                ('profile_label_set', models.CharField(default='A', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ShamQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right_end', models.CharField(default='right', max_length=200)),
                ('left_end', models.CharField(default='left', max_length=200)),
                ('sham_name', models.CharField(default='Name', max_length=200)),
                ('label_set', models.CharField(default='A', max_length=2)),
                ('question_heb_male', models.CharField(default='Default question?', max_length=200)),
                ('question_heb_female', models.CharField(default='Default question?', max_length=200)),
                ('presenting_name', models.CharField(default='Default Name', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserToSubjectIPA2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_num', models.CharField(default='not provided', max_length=100)),
                ('features_set', models.CharField(default='A', max_length=100)),
                ('education', models.CharField(default='BA', max_length=100)),
                ('age', models.IntegerField(default=999)),
                ('gender', models.CharField(default='female', max_length=100)),
                ('runningLocation', models.CharField(default='Lab', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SimilarityContextModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_set', models.CharField(default='A', max_length=2)),
                ('context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.context')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction_text', models.CharField(default='', max_length=2000)),
                ('int_place', models.IntegerField()),
                ('is_in_order', models.BooleanField(default=True)),
                ('off_order_place', models.CharField(default='irrelevant', max_length=40)),
                ('instruction_text_male', models.CharField(default='', max_length=2000)),
                ('instruction_text_female', models.CharField(default='', max_length=2000)),
                ('pitctures_names', models.CharField(default='', max_length=1000)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.experiment')),
                ('str_phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.experimentphase')),
            ],
        ),
        migrations.CreateModel(
            name='GameMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(default='no assigned name', max_length=30)),
                ('ps_threshold', models.FloatField()),
                ('is_subject_play_row', models.BooleanField(default=True)),
                ('cooperation_row', models.FloatField(default=0)),
                ('cooperation_col', models.FloatField(default=0)),
                ('strategy_a', models.CharField(default='cooperate', max_length=30)),
                ('strategy_b', models.CharField(default='defect', max_length=30)),
                ('pA_Aa', models.IntegerField(default=1)),
                ('pB_Aa', models.IntegerField(default=2)),
                ('pA_Ab', models.IntegerField(default=3)),
                ('pB_Ab', models.IntegerField(default=4)),
                ('pA_Ba', models.IntegerField(default=5)),
                ('pB_Ba', models.IntegerField(default=6)),
                ('pA_Bb', models.IntegerField(default=7)),
                ('pB_Bb', models.IntegerField(default=8)),
                ('context_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.context')),
                ('phase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipa_2.experimentphase')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0.5)),
                ('label_set', models.CharField(default='A', max_length=2)),
                ('feature_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.featurelabels')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.similaritycontextmodel')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('target_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.featurelabels')),
                ('target_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.profilemodel')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('profilemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ipa_2.profilemodel')),
                ('subject_num', models.CharField(default='not_provided', max_length=50)),
                ('completed_experiments', models.CharField(default='-', max_length=500)),
                ('subject_session', models.IntegerField(default=0)),
                ('max_similarity_value', models.IntegerField(default=999)),
                ('min_similarity_value', models.IntegerField(default=999)),
                ('max_similarity_name', models.CharField(default='not_provided', max_length=50)),
                ('min_similarity_name', models.CharField(default='not_provided', max_length=50)),
                ('trials_string_list', models.TextField(default='-')),
                ('trials_games_names', models.TextField(default='-')),
                ('trials_responses_list', models.TextField(default='-')),
                ('profiles_response_times', models.TextField(default='-')),
                ('feature_response_times', models.TextField(default='-')),
                ('trial_features_order', models.TextField(default='-')),
                ('subject_profile_sides', models.TextField(default='-')),
                ('subject_reported_sides', models.TextField(default='-')),
                ('identification_rts', models.TextField(default='-')),
                ('identification_profiles', models.TextField(default='-')),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('gender', models.CharField(default='male', max_length=20)),
                ('age', models.IntegerField(default=999)),
                ('education', models.CharField(default='BA', max_length=20)),
                ('n_identification_task_rounds', models.IntegerField(default=0)),
                ('runningLocation', models.CharField(default='Lab', max_length=20)),
                ('session_1_ps', models.FloatField(default=0.5)),
                ('session_2_ps', models.FloatField(default=0.5)),
                ('subject_ps', models.FloatField(default=0.1)),
                ('context_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipa_2.context')),
                ('current_phase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipa_2.experimentphase')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.experiment')),
            ],
            bases=('ipa_2.profilemodel',),
        ),
        migrations.CreateModel(
            name='MinMaxProfileModel',
            fields=[
                ('profilemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ipa_2.profilemodel')),
                ('target_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.subject')),
            ],
            bases=('ipa_2.profilemodel',),
        ),
        migrations.CreateModel(
            name='ArtificialProfileModel',
            fields=[
                ('profilemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ipa_2.profilemodel')),
                ('target_phase', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ipa_2.experimentphase')),
                ('target_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipa_2.subject')),
            ],
            bases=('ipa_2.profilemodel',),
        ),
    ]
