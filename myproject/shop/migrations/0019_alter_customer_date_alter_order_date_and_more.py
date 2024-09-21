# Generated by Django 5.0.6 on 2024-08-29 01:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_customer_date_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 32, 54, 923878)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 32, 54, 924876)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 21, 32, 54, 923878)),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='products',
            field=models.ManyToManyField(through='shop.InvoiceProduct', to='shop.product'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
        ),
    ]
