# Generated by Django 4.2.5 on 2023-11-29 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0010_price_change_old_income_alter_price_change_income'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='providers',
            new_name='provider',
        ),
    ]
