# Generated by Django 5.0.6 on 2024-08-30 02:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_remove_productimage_alt_text_alter_customer_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 29, 22, 23, 18, 531305)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 29, 22, 23, 18, 531305)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 29, 22, 23, 18, 531305)),
        ),
    ]