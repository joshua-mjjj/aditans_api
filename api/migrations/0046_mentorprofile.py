# Generated by Django 3.2.8 on 2022-04-06 09:14

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_alter_user_account_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('latitude', models.FloatField(max_length=9)),
                ('longitude', models.FloatField(max_length=9)),
                ('minimum_team', models.IntegerField()),
                ('maximum_team', models.IntegerField()),
                ('years_of_experience', models.CharField(max_length=10)),
                ('business_name', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=api.models.upload_path)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.projecttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
