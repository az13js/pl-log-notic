# Generated by Django 3.1 on 2020-10-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pltplconf', '0005_auto_20201006_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pltasksetting',
            name='task_name',
            field=models.CharField(default='', max_length=64, unique=True, verbose_name='任务名称'),
        ),
    ]
