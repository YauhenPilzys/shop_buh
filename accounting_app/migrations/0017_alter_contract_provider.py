# Generated by Django 4.2.5 on 2024-04-02 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0016_alter_contract_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting_app.provider', verbose_name='Поставщик'),
        ),
    ]
