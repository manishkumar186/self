# Generated by Django 3.0.6 on 2021-02-03 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0004_register_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='add_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250)),
                ('product_price', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('product_image', models.ImageField(upload_to='products/%Y/%m/%d')),
                ('details', models.TextField()),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Category')),
                ('seller_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]