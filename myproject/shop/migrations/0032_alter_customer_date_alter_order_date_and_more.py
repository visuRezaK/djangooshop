# Generated by Django 5.0.6 on 2024-09-21 02:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_alter_customer_date_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 9, 20, 22, 42, 49, 724802)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 9, 20, 22, 42, 49, 725885)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 9, 20, 22, 42, 49, 725885)),
        ),
    ]
