# Generated by Django 4.2.3 on 2023-10-25 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pref_app', '0004_alter_pref_colleges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pref',
            name='colleges',
        ),
        migrations.RemoveField(
            model_name='pref',
            name='mealtimes',
        ),
        migrations.AddField(
            model_name='pref',
            name='breakfast',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pref',
            name='brunch_lunch',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pref',
            name='dinner',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
