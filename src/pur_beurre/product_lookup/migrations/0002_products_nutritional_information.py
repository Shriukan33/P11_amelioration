# Generated by Django 3.2.9 on 2022-02-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_lookup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='nutritional_information',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]