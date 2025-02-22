# Generated by Django 5.1.6 on 2025-02-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='month',
            field=models.IntegerField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], default=2),
        ),
        migrations.AddField(
            model_name='budget',
            name='year',
            field=models.IntegerField(default=2025),
        ),
    ]
