# Generated by Django 5.0.6 on 2024-09-07 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_invoice_invoiceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]