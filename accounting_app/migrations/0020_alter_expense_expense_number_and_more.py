# Generated by Django 4.2.5 on 2023-10-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0019_alter_expense_expense_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_number',
            field=models.PositiveIntegerField(default=0, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.PositiveIntegerField(default=0, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество товара'),
        ),
    ]