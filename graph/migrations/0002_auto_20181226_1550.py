# Generated by Django 2.1.4 on 2018-12-26 22:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instacategories',
            name='catarray',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=80), size=80),
        ),
    ]
