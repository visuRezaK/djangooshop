# Generated by Django 5.0.6 on 2024-08-29 01:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_customer_date_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 38, 58, 767829)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 38, 58, 767829)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 38, 58, 767829)),
        ),
    ]