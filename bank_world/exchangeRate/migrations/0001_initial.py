# Generated by Django 5.1.3 on 2024-11-29 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50, null='false')),
                ('currency', models.CharField(max_length=50, null='false')),
                ('sellingPrice', models.FloatField(null='false')),
                ('buyingPrice', models.FloatField(null='false')),
                ('averagePrice', models.FloatField(null='false')),
                ('lastUpdate', models.CharField(max_length=30)),
            ],
        ),
    ]