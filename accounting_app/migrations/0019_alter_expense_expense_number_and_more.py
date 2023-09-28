# Generated by Django 4.2.5 on 2023-10-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0018_alter_price_change_price_change_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_number',
            field=models.IntegerField(default=0, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.IntegerField(default=0, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product_quantity',
            field=models.IntegerField(default=0, verbose_name='Количество товара'),
        ),
    ]
