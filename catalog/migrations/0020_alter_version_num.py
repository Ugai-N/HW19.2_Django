# Generated by Django 4.2.4 on 2023-09-25 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_version_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='num',
            field=models.IntegerField(auto_created=True, default=1, verbose_name='Номер'),
        ),
    ]
