# Generated by Django 2.2.2 on 2019-06-29 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20190629_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='down_votes',
            new_name='total_votes',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='down_votes',
            new_name='total_votes',
        ),
    ]