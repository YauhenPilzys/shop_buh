# Generated by Django 4.2.5 on 2023-11-21 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0003_price_change_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='print',
            field=models.CharField(default=2, max_length=100, verbose_name='Печать true/false'),
            preserve_default=False,
        ),
    ]