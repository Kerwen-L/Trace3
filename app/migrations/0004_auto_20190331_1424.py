# Generated by Django 2.1.7 on 2019-03-31 06:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20190330_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerregistry',
            name='RegisterTimeConsumer',
            field=models.DateField(default=datetime.date(2019, 3, 31)),
        ),
    ]
