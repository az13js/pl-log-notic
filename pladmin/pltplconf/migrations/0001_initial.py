# Generated by Django 3.1 on 2020-08-31 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pljob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_exec_time', models.DateTimeField(verbose_name='最后一次执行时间')),
                ('next_exec_time', models.DateTimeField(verbose_name='下一次执行时间')),
                ('delay_sec', models.IntegerField(verbose_name='延迟的时间（秒）')),
                ('job_name', models.CharField(max_length=100, verbose_name='任务名称')),
                ('wx_address', models.URLField(max_length=400, verbose_name='消息通知地址')),
            ],
        ),
    ]
