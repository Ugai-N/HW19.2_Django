# Generated by Django 4.2.4 on 2023-09-05 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_contacts_tax_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='create_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='change_date',
            new_name='updated_at',
        ),
    ]
