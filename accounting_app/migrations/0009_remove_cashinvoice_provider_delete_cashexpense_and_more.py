# Generated by Django 4.2.5 on 2024-01-12 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0008_cashinvoice_cashexpense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashinvoice',
            name='provider',
        ),
        migrations.DeleteModel(
            name='CashExpense',
        ),
        migrations.DeleteModel(
            name='CashInvoice',
        ),
    ]