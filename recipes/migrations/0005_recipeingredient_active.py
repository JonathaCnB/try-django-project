# Generated by Django 3.2.7 on 2021-10-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipeingredient_quantity_as_float'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
