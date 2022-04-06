# Generated by Django 3.2.8 on 2022-04-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_alter_user_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('normal_user', 'Normal User'), ('mentor', 'Mentor'), ('premium_normal_user', 'Premium Normal User')], max_length=32),
        ),
    ]
