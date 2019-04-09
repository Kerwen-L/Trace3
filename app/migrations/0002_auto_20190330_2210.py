# Generated by Django 2.1.7 on 2019-03-30 14:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerregistry',
            name='RegisterTimeConsumer',
            field=models.DateField(default=datetime.date(2019, 3, 30)),
        ),
        migrations.AlterField(
            model_name='processorregistry',
            name='HC4foodCertificationNo',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='processorregistry',
            name='HC4foodCertificationSrc',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processorregistry',
            name='ProcessorCounts',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='processorregistry',
            name='WorkPlaceID',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transportdata',
            name='Flag',
            field=models.IntegerField(default=0),
        ),
    ]