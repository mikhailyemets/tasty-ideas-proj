# Generated by Django 5.0.6 on 2024-05-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasty_ideas', '0002_alter_category_dish_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='dish_type',
            field=models.CharField(choices=[('sushi', 'sushi rolls'), ('salad', 'different salads'), ('soup', 'soups')], max_length=50),
        ),
    ]
