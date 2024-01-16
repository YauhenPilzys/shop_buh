# Generated by Django 4.2.5 on 2024-01-16 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0011_alter_expense_provider_alter_income_invoice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting_app.provider', verbose_name='Поставщик'),
        ),
        migrations.AlterField(
            model_name='expense_item',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting_app.expense', verbose_name='Расходная накладная'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='providers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting_app.provider', verbose_name='Поставщик'),
        ),
    ]
