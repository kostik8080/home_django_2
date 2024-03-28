# Generated by Django 4.2 on 2024-03-26 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_is_published', 'can publish product'), ('change_discription', 'can change product description'), ('change_category', 'can change product category')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]
