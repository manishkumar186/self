# Generated by Django 3.0.6 on 2021-03-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_order_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email_address',
            field=models.EmailField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]