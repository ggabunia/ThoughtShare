# Generated by Django 2.1.3 on 2018-12-02 01:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('idea_app', '0014_auto_20181201_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='idearating',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
