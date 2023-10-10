# Generated by Django 4.2.5 on 2023-10-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0002_rename_clients_expense_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='expense_price_allowance',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10, verbose_name='Стоимость с надбавкой'),
            preserve_default=False,
        ),
    ]