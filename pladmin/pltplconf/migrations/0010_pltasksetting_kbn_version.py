# Generated by Django 3.1 on 2020-10-12 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pltplconf', '0009_plpushlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='pltasksetting',
            name='kbn_version',
            field=models.CharField(default='', max_length=15, verbose_name='Kibana版本号'),
        ),
    ]
