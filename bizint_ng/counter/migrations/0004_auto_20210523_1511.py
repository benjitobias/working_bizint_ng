# Generated by Django 3.1.5 on 2021-05-23 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_action_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='note',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='count',
            name='update_week',
            field=models.IntegerField(default=20, verbose_name='Week in year'),
        ),
    ]
