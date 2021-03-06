# Generated by Django 2.0.6 on 2018-08-21 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('남', '남자'), ('여', '여자')], default='남', max_length=1)),
                ('birthday', models.DateField()),
                ('homeplace', models.CharField(max_length=15)),
                ('workplace', models.CharField(max_length=15)),
                ('favorite', models.CharField(max_length=25)),
                ('introduction', models.TextField()),
                ('joindate', models.DateField(default=datetime.date.today)),
                ('recentdate', models.DateField(default=datetime.date.today)),
                ('times', models.IntegerField(default=0)),
            ],
        ),
    ]
