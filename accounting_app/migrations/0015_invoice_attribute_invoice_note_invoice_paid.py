# Generated by Django 4.2.5 on 2024-02-19 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0014_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='attribute',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Признак'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Оплачено True/False'),
        ),
    ]
