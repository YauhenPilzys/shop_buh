# Generated by Django 4.2.5 on 2023-10-02 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0014_alter_expense_expense_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_date',
            field=models.DateField(default=2, verbose_name='Дата продажи'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_number',
            field=models.IntegerField(default=0, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='product_date',
            field=models.DateField(default=2, verbose_name='Дата поступления товара'),
            preserve_default=False,
        ),
    ]