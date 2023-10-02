# Generated by Django 4.2.5 on 2023-10-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0012_price_change_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price_change',
            name='expense_sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Старая цена со склада'),
        ),
    ]