# Generated by Django 3.0 on 2021-06-17 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_hook', '0007_auto_20210614_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stripepayment',
            name='card_number',
        ),
    ]
