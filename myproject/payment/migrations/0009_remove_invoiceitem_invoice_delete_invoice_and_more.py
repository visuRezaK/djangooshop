# Generated by Django 5.0.6 on 2024-09-21 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_orderitem_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitem',
            name='invoice',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='InvoiceItem',
        ),
    ]