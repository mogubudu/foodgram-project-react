# Generated by Django 3.2 on 2023-08-13 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientamount',
            options={'verbose_name': 'Количество ингредиента', 'verbose_name_plural': 'Количество ингредиента'},
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),
    ]
