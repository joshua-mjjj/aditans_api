# Generated by Django 3.2.8 on 2022-04-06 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_user_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('normal_user', 'Normal User'), ('mentor', 'Mentor'), ('premiuim_normal_user', 'Premiuim Normal User')], max_length=32),
        ),
    ]
