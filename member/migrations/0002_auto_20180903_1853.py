# Generated by Django 2.0.6 on 2018-09-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='recentdate',
            field=models.DateField(),
        ),
    ]
