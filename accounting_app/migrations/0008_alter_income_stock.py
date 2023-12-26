# Generated by Django 4.2.5 on 2023-11-28 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0007_alter_income_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='stock',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounting_app.stock', verbose_name='Склад'),
        ),
    ]
