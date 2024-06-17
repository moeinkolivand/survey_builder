# Generated by Django 5.0.6 on 2024-06-17 18:34

import django.contrib.postgres.fields.hstore
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('question_type', models.CharField(choices=[('text', 'TEXT'), ('multiple_choice', 'MULTIPLE_CHOICE'), ('rating', 'RATING'), ('contact_information', 'CONTACT_INFORMATION')], max_length=20, verbose_name='question_type')),
                ('order', models.IntegerField(verbose_name='order')),
                ('validation_rules', models.JSONField(blank=True, default=dict, verbose_name='validations')),
                ('data', models.JSONField(verbose_name='question data')),
                ('media', models.ImageField(blank=True, upload_to='question_media/', verbose_name='media')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_archive', models.BooleanField(default=False, verbose_name='is archive')),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
                'db_table': 'survey',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.IntegerField(default=1)),
                ('user_answer', django.contrib.postgres.fields.hstore.HStoreField(default=dict, verbose_name='user answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.question', verbose_name='question')),
            ],
            options={
                'verbose_name': 'answers',
                'verbose_name_plural': 'answers',
                'db_table': 'answer',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey', verbose_name='survey'),
        ),
    ]
