# Generated by Django 3.0 on 2021-05-26 14:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(default=uuid.UUID('a546cec3-d4d7-43da-b9c5-ffb5d1c7a8ab')),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('26e5b21c-1d8e-400c-af83-ab65fc046775'), max_length=250),
        ),
    ]
