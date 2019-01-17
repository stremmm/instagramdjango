# Generated by Django 2.1.4 on 2018-12-26 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.IntegerField()),
                ('substart', models.DateTimeField()),
                ('subend', models.DateTimeField()),
                ('active', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('isrunning', models.BooleanField()),
                ('accountuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Subscriptions',
                'db_table': 'Subscription',
                'managed': True,
            },
        ),
    ]
