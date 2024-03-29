# Generated by Django 4.2.5 on 2024-01-11 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0005_expense_expense_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='client',
        ),
        migrations.AddField(
            model_name='expense',
            name='provider',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounting_app.provider', verbose_name='Поставщик'),
            preserve_default=False,
        ),
    ]
