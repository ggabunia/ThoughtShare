# Generated by Django 2.1.3 on 2018-11-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea_app', '0007_auto_20181125_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='i_auction',
            new_name='i_is_auction',
        ),
        migrations.AddField(
            model_name='idea',
            name='i_auction_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]